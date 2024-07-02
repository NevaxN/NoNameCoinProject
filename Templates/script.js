document.getElementById('listar-clientes-btn').addEventListener('click', listarClientes);
document.getElementById('adicionar-cliente-form').addEventListener('submit', adicionarCliente);
document.getElementById('editar-cliente-form').addEventListener('submit', editarCliente);
document.getElementById('excluir-cliente-form').addEventListener('submit', excluirCliente);
document.getElementById('listar-transacoes-btn').addEventListener('click', listarTransacoes);
document.getElementById('adicionar-transacao-form').addEventListener('submit', adicionarTransacao);

function listarClientes() {
    fetch('http://127.0.0.1:5000/cliente')
        .then(response => response.json())
        .then(data => {
            console.log('Dados recebidos para clientes:', data); // Adicionado para depuração
            const lista = document.getElementById('clientes-lista');
            lista.innerHTML = '';
            if (data.Clientes) {
                data.Clientes.forEach(cliente => {
                    const item = document.createElement('li');
                    item.textContent = `ID: ${cliente.id}, Nome: ${cliente.nome}, Moedas: ${cliente.qtdMoeda}`;
                    lista.appendChild(item);
                });
            }
        })
        .catch(error => console.error('Erro:', error));
}

function adicionarCliente(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const senha = document.getElementById('senha').value;
    const qtdMoeda = document.getElementById('qtdMoeda').value;

    fetch(`http://127.0.0.1:5000/cliente/${nome}/${senha}/${qtdMoeda}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Sucesso:', data);
            listarClientes();
        })
        .catch(error => console.error('Erro:', error));
}

function editarCliente(event) {
    event.preventDefault();

    const id = document.getElementById('id-editar').value;
    const nome = document.getElementById('nome-editar').value;
    const senha = document.getElementById('senha-editar').value;
    const qtdMoeda = document.getElementById('qtdMoeda-editar').value;

    fetch(`http://127.0.0.1:5000/cliente/${id}/${nome}/${senha}/${qtdMoeda}`, {
        method: 'PUT',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Sucesso:', data);
            listarClientes();
        })
        .catch(error => console.error('Erro:', error));
}

function excluirCliente(event) {
    event.preventDefault();

    const id = document.getElementById('id-excluir').value;

    fetch(`http://127.0.0.1:5000/cliente/${id}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Sucesso:', data);
            listarClientes();
        })
        .catch(error => console.error('Erro:', error));
}

function listarTransacoes() {
    fetch('http://127.0.0.1:5000/transacoes')
        .then(response => response.json())
        .then(data => {
            console.log('Dados recebidos para transações:', data); // Adicionado para depuração
            const lista = document.getElementById('transacoes-lista');
            lista.innerHTML = '';
            if (data.Transações) {
                data.Transações.forEach(transacao => {
                    const item = document.createElement('li');
                    item.textContent = `ID: ${transacao.id}, Cliente: ${transacao.idCliente}, Descrição: ${transacao.descricao}, Valor: ${transacao.valor}`;
                    lista.appendChild(item);
                });
            }
        })
        .catch(error => console.error('Erro:', error));
}

function adicionarTransacao(event) {
    event.preventDefault();

    const idCliente = document.getElementById('idCliente').value;
    const descricao = document.getElementById('descricao').value;
    const valor = document.getElementById('valor').value;

    fetch(`http://127.0.0.1:5000/transacao/${idCliente}/${descricao}/${valor}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Sucesso:', data);
            listarTransacoes();
        })
        .catch(error => console.error('Erro:', error));
}
