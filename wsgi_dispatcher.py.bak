import os
import importlib.util
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask


def load_module_app(module_name, app_py_path):
    """Dynamically load a module file and return its `app` Flask object if present."""
    try:
        spec = importlib.util.spec_from_file_location(f"nexora_module_{module_name}", app_py_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, 'app', None)
    except Exception:
        return None


def create_dispatch_app():
    apps_root = os.path.join(os.path.dirname(__file__), 'apps')
    mount_map = {}

    # attempt to load the home app from known candidates
    home_app = None
    for candidate in ('nexora-home', 'nexora_home', 'nexorahome'):
        p = os.path.join(apps_root, candidate)
        app_py = os.path.join(p, 'app.py')
        if os.path.exists(app_py):
            home_app = load_module_app('nexora_home', app_py)
            home_dir_name = candidate
            break

    # iterate over app folders and try to load app.py for mounting
    for name in sorted(os.listdir(apps_root)):
        path = os.path.join(apps_root, name)
        if not os.path.isdir(path):
            continue
        app_py = os.path.join(path, 'app.py')
        if os.path.exists(app_py):
            # skip the one we selected as home (if any)
            if 'home_dir_name' in locals() and name == home_dir_name:
                continue
            loaded = load_module_app(name.replace('-', '_'), app_py)
            if loaded:
                # mount under /<module_name> so home remains at /
                prefix = f"/{name}"
                mount_map[prefix] = loaded

    # If no explicit home app found, pick the first loaded app as home
    if home_app is None:
        if mount_map:
            # pop one entry to be home
            first_prefix, first_app = mount_map.popitem()
            home_app = first_app
        else:
            # fallback: simple empty Flask app
            fallback = Flask('nexora_fallback')
            @fallback.route('/')
            def index():
                return 'Nexora Suite - no home app found', 200
            home_app = fallback

    return DispatcherMiddleware(home_app, mount_map)


application = create_dispatch_app()

if __name__ == '__main__':
    # quick server for local testing
    from werkzeug.serving import run_simple
    print('Mount points:')
    # application.mounts is an internal mapping, but print keys from implementation
    run_simple('0.0.0.0', 8080, application, use_reloader=True)
