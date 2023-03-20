import product_catalog
import transformer
import integrator
from app import validate_integration

def development():
    transformer.start()
    product_catalog.start_config()
    integrator.start()
    validate_integration.start()
    pass

if __name__ == '__main__':
   development()
