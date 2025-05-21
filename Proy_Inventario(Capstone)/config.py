# Modificado para proy





import os

class Config:
    """
    Configuración general de la aplicación Flask.
    Puede extenderse a diferentes entornos (Desarrollo, Producción, etc.).
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', '30102001R00572231')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost/inventario_personal'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False