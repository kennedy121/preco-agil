
from config import Config

def inject_global_vars():
    """
    Injeta variáveis globais de configuração em todos os templates.
    Isso evita ter que passar essas variáveis em cada chamada `render_template`.
    """
    return {
        'app_version': Config.APP_VERSION,
        'app_description': Config.APP_DESCRIPTION,
        'app_name': Config.APP_NAME
    }
