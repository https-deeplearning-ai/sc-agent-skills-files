"""
MinerU API Client Example
=========================

Example client for interacting with MinerU API server.

Usage:
    python client_example.py <server-url> <pdf-file>
    python client_example.py http://localhost:8000 document.pdf
"""

import requests
import sys
from pathlib import Path


def parse_pdf_via_api(
    pdf_path: str,
    server_url: str = "http://localhost:8000",
    backend: str = "hybrid-auto-engine",
    language: str = "en"
):
    """
    Send PDF to API server for processing.

    Args:
        pdf_path: Path to local PDF file
        server_url: API server URL
        backend: Processing backend
        language: Language code

    Returns:
        Markdown content or None if failed
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"❌ Error: File not found: {pdf_path}")
        return None

    print(f"📤 Uploading: {pdf_file.name}")
    print(f"🌐 Server: {server_url}")
    print(f"⚙️  Backend: {backend}")
    print(f"🌍 Language: {language}\n")

    # Open file and send to API
    with open(pdf_file, 'rb') as f:
        files = {'file': (pdf_file.name, f, 'application/pdf')}
        data = {
            'backend': backend,
            'language': language
        }

        try:
            response = requests.post(
                f"{server_url}/parse",
                files=files,
                data=data,
                timeout=300  # 5 minutes timeout
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"📄 Filename: {result['filename']}")
                print(f"📊 Content length: {result['metadata']['content_length']} chars")
                print(f"🖼️  Images: {result['metadata']['num_images']}")
                print(f"\n--- Markdown Preview (first 500 chars) ---")
                print(result['markdown'][:500])
                if len(result['markdown']) > 500:
                    print("...\n")
                return result['markdown']
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.json()}")
                return None

        except requests.exceptions.Timeout:
            print(f"❌ Error: Request timed out")
            return None
        except requests.exceptions.ConnectionError:
            print(f"❌ Error: Could not connect to server at {server_url}")
            print(f"   Make sure the server is running!")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


def batch_parse_pdfs(pdf_files: list, server_url: str = "http://localhost:8000"):
    """
    Parse multiple PDFs via API.

    Args:
        pdf_files: List of PDF file paths
        server_url: API server URL
    """
    print(f"📚 Batch processing {len(pdf_files)} PDFs\n")

    # Prepare files
    files = []
    for pdf_path in pdf_files:
        pdf_file = Path(pdf_path)
        if pdf_file.exists():
            files.append(('files', (pdf_file.name, open(pdf_file, 'rb'), 'application/pdf')))

    data = {
        'backend': 'hybrid-auto-engine',
        'language': 'en'
    }

    try:
        response = requests.post(
            f"{server_url}/parse-batch",
            files=files,
            data=data,
            timeout=600  # 10 minutes for batch
        )

        # Close file handles
        for _, (_, file_obj, _) in files:
            file_obj.close()

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch complete!")
            print(f"📊 Total: {result['total']}")
            print(f"\nResults:")
            for r in result['results']:
                status_icon = "✅" if r['status'] == 'success' else "❌"
                print(f"  {status_icon} {r['filename']}: {r['status']}")
                if r['status'] == 'success':
                    print(f"     Length: {r['content_length']} chars")
        else:
            print(f"❌ Batch failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Error: {e}")


def check_health(server_url: str = "http://localhost:8000"):
    """Check if API server is healthy."""
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Server is healthy")
            return True
        else:
            print(f"⚠️  Server returned: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {server_url}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client_example.py <server-url> <pdf-file>")
        print("\nExamples:")
        print("  python client_example.py http://localhost:8000 document.pdf")
        print("  python client_example.py http://192.168.1.100:8000 paper.pdf")
        print("\nFirst, start the server:")
        print("  python api_server.py")
        sys.exit(1)

    server_url = sys.argv[1]
    pdf_file = sys.argv[2]

    # Check server health
    if check_health(server_url):
        print()
        # Parse PDF
        parse_pdf_via_api(pdf_file, server_url)
