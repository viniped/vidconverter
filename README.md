VidConverter

Introdução
O script VidConverter é um script em Python que permite ao usuário converter arquivos de vídeo em uma pasta de entrada especificada para o formato MP4 usando a biblioteca FFmpeg. 

Requisitos
Antes de usar o script VidConverter, você precisa ter o seguinte instalado:

Python 3.7.x

FFmpeg: Certifique-se de que o executável do FFmpeg esteja disponível no PATH do sistema.
Bibliotecas Utilizadas


Funcionamento: 

Solicita ao usuário para inserir o caminho da pasta de entrada contendo os arquivos de vídeo a ser convertido.
Define o caminho da pasta de saída como um subdiretório chamado "output" dentro do diretório do script.
Itera por todas as subpastas e arquivos na pasta de entrada
Verifica se cada arquivo é um arquivo de vídeo com extensões válidas.
Converte cada arquivo de vídeo para o formato MP4 usando o FFmpeg e o salva na pasta de saída.
Remove o arquivo de vídeo original após a conversão.


Observação: A ferramenta de linha de comando ffmpeg é usada para a conversão de vídeo, portanto, certifique-se de que ela está corretamente instalada e acessível no PATH do sistema.


Como Usar
Certifique-se de ter o Python 3.x e o FFmpeg instalados em seu sistema.
Instale as bibliotecas Python necessárias executando: pip install tqdm colorama pyfiglet ou use o arquivo update_libs.bat .
Copie o script VidConverter para um diretório onde deseja converter arquivos de vídeo.
Execute o script usando: python vid_converter.py.


O script exibirá um banner colorido e solicitará que você insira o caminho da pasta de entrada.
Após fornecer o caminho da pasta, o script converterá todos os arquivos de vídeo na pasta de entrada para o formato MP4 e os salvará no subdiretório "output".
Importante: Certifique-se sempre de fazer backup de seus arquivos de vídeo antes de executar o script, pois ele removerá os arquivos originais após a conversão.

Aviso Legal:

O script VidConverter é fornecido "como está" e sem garantias. É sua responsabilidade garantir que você tenha os direitos e permissões necessários para realizar conversões de vídeo nos arquivos da pasta de entrada especificada. O autor do script não assume nenhuma responsabilidade por qualquer uso indevido ou danos causados pelo uso deste script.
