from app import create_app
from deploy import check_and_deploy

app = create_app()

if __name__ == '__main__':
    # Check for contract updates before starting server
    check_and_deploy()
    app.run(host='0.0.0.0', port=5000, debug=True)
