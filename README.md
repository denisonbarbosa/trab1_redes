# trab1_redes
Obs.: Os comentários e docstrings foram escritos em inglês por preferência dos
autores. Esperamos que não tenha problema.

Para executar os arquivos Peer.py, utilize:
python Peer.py <ip_peer> <porta_udp> <porta_tcp>

Após isso, siga os comandos exibidos no menu.

Legenda para os tipos das mensagens (para facilitar compreensão do log):
  Requisições:
    1 -> Requisição para listagem de IPs
    2 -> Requisição para listagem de arquivos
    3 -> Requisição de busca de um arquivo
    4 -> Requisição para baixar um arquivo
  
  Respostas:
    01 -> Resposta à requisição de listagem de ips
    02 -> Resposta à requisição de listagem de arquivos
    03 -> Resposta à requisição de busca de um arquivo
    04 -> Resposta à requisição de baixar um arquivo

  Apesar de não ser o jeito mais efetivo de representar um tipo, decidimos fazer
  dessa forma para facilitar a compreensão das mensagens.