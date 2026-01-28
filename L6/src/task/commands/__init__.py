import typer

from .add import app as add_app
from .done import app as done_app
from .list import app as list_app

app = typer.Typer(help="Task manager CLI.", no_args_is_help=True)

# Single commands - flattens to top level
app.add_typer(add_app)
app.add_typer(done_app)
app.add_typer(list_app)
