#!/bin/bash

# Função para lidar com o sinal SIGINT (Ctrl+C)
function handle_interrupt {
    echo "Recebido sinal de interrupção. Encerrando scripts $pid_script1 $pid_script2 $pid_script3..."
    
    # Encerrar o primeiro script Python (se estiver em execução)
    if [ -n "$pid_script1" ]; then
        kill -SIGTERM -P "$pid_script1"  # Envie um sinal de interrupção
        wait "$pid_script1"  # Aguarde a conclusão
    fi

    # Encerrar o segundo script Python (se estiver em execução)
    if [ -n "$pid_script2" ]; then
        kill -SIGTERM -P "$pid_script2"  # Envie um sinal de interrupção
        wait "$pid_script2"  # Aguarde a conclusão
    fi

    # Encerrar o script React (se estiver em execução)
    if [ -n "$pid_script2" ]; then
        kill -SIGTERM -P "$pid_script3"  # Envie um sinal de interrupção
        wait "$pid_script2"  # Aguarde a conclusão
    fi

    echo "Scripts encerrados. Saindo."
    exit 1
}

# Capturar o sinal SIGINT (Ctrl+C)
trap 'handle_interrupt' SIGINT

# Caminho para os scripts Python
caminho_script1="./src/FlaskApp/main.py"
caminho_script2="./src/ZmqServer/main.py"

# Executar o primeiro script em segundo plano
python3 "$caminho_script1" &
pid_script1=$!

# Executar o segundo script em segundo plano
python3 "$caminho_script2" &
pid_script2=$!

cd src/chatbot-frontend

yarn start > logs/yarn.log &
pid_script3=$!

# Aguardar a conclusão de ambos os scripts
wait "$pid_script1"
wait "$pid_script2"
wait "$pid_script3"

echo "Ambos os scripts foram executados em paralelo."

