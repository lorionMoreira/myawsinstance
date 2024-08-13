from fastapi import FastAPI, Request, HTTPException
import subprocess
import hmac
import hashlib
import os

app = FastAPI()

# Substitua pelo seu segredo do webhook do GitHub
GITHUB_SECRET = os.getenv('GITHUB_SECRET2', 'fndopnfdopHFOEIRYUTOERPBVNKCDSQds')

@app.post("/update-project")
async def update_project(request: Request):
    # Verificar a assinatura do GitHub
    try:
        signature = request.headers.get('X-Hub-Signature-256')
        if signature is None:
            raise HTTPException(status_code=400, detail="Missing signature")

        body = await request.body()
        hashhex = hmac.new(GITHUB_SECRET.encode(), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(f'sha256={hashhex}', signature):
            raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signature verification failed: {str(e)}")

    # Caminhos dos diretórios
    project_path = "/home/ubuntu/projects/makeponto"
    backend_path = "/home/ubuntu/projects/makeponto/backend"
    jar_path = "/srv/vendas/vendas-1.0-SNAPSHOT.jar"
    target_jar_path = "/home/ubuntu/projects/makeponto/backend/target/vendas-1.0-SNAPSHOT.jar"

    # Função para executar comandos
    def run_command(command, cwd=None):
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.stdout + result.stderr

    # 1. Deletar arquivo jar
    delete_jar = run_command(f"sudo rm {jar_path}")

    # 2. Executar 'git status'
    git_status = run_command("git status", project_path)
    
    # 3. Executar 'git pull origin main'
    git_pull = run_command("git pull origin main", project_path)
    
    # 4. Executar 'mvn clean package'
    mvn_package = run_command("mvn clean package", backend_path)
    
    # 5. Copiar o arquivo jar
    copy_jar = run_command(f"cp {target_jar_path} {jar_path}")
    
    # 6. Mudar a propriedade do arquivo jar copiado
    change_ownership = run_command(f"sudo chown vendasuser:vendasuser {jar_path}")
    
    # 7. Deletar o arquivo jar no diretório target
    delete_target_jar = run_command(f"rm {target_jar_path}")

    # 8. Reiniciar o serviço
    restart_service = run_command("sudo systemctl restart vendas.service")

    # Retornar as respostas dos comandos
    return {
        "delete_jar": delete_jar,
        "git_status": git_status,
        "git_pull": git_pull,
        "mvn_package": mvn_package,
        "copy_jar": copy_jar,
        "change_ownership": change_ownership,
        "delete_target_jar": delete_target_jar,
        "restart_service": restart_service
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
