import cv2
from ultralytics import YOLO

# Carrega o modelo treinado
model = YOLO('model/cartas2110.pt')

# Abre o vídeo para processamento
#video = cv2.VideoCapture('video/truco2.mp4')
video = cv2.VideoCapture(0)

# Verifica se o vídeo foi aberto corretamente
if not video.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Obtém informações sobre o vídeo
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

# Define o codec e cria o objeto VideoWriter para salvar o vídeo
output_video = cv2.VideoWriter('video/saved_truco.avi',
                               cv2.VideoWriter_fourcc(*'XVID'),
                               fps, (frame_width, frame_height))

while True:
    # Lê um frame do vídeo
    check, img = video.read()
    if not check:  # Se não conseguir ler o frame, interrompe o loop
        print("Não foi possível ler o frame. Finalizando...")
        break

    # Realiza a predição utilizando o modelo YOLO
    results = model.predict(img, verbose=False, save=True)

    # Itera sobre os resultados de detecção
    for obj in results:
        nomes = obj.names  # Obtém os nomes das classes

        # Para cada bounding box detectada
        for item in obj.boxes:
            # Converte as coordenadas para inteiros
            x1, y1, x2, y2 = item.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Identifica a classe do objeto
            cls = int(item.cls[0])
            nomeClasse = nomes[cls]

            # Confiança da predição
            conf = round(float(item.conf[0]), 2)
            texto = f'{nomeClasse} - {conf}'

            # Adiciona o texto na imagem
            cv2.putText(img, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            # Desenha um retângulo em torno do objeto com base na classe
            if nomeClasse == '10' or nomeClasse == '2' or nomeClasse == '3' or nomeClasse == '4' or nomeClasse == '5' or nomeClasse == '6':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            elif nomeClasse == '7' or nomeClasse == '8' or nomeClasse == '9' or nomeClasse == 'A' or nomeClasse == 'J' or nomeClasse == 'Q' or nomeClasse == 'K':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            elif nomeClasse == 'spade' or nomeClasse == 'club':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 3)
            elif nomeClasse == 'heart' or nomeClasse == 'diamond':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

    # Exibe o frame com as detecções
    cv2.imshow('IMG', img)

    # Escreve o frame no vídeo de saída
    output_video.write(img)

    # Sai do loop se a tecla 'ESC' for pressionada
    if cv2.waitKey(1) == 27:
        break

# Libera o vídeo, o vídeo de saída e fecha as janelas
video.release()
output_video.release()
cv2.destroyAllWindows()