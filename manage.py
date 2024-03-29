import os
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from app import create_app

app = create_app()

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main(['tests', '-q'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print("running manager ..")
    manager.run()
