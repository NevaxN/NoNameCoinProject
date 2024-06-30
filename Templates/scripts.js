let clientes = [];
let seletores = [];
let transacoes = [];

document.getElementById('clienteForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const nome = document.getElementById('clienteNome').value;
    const senha = document.getElementById('clienteSenha').value;
    const moedas = document.getElementById('clienteMoedas').value;

    const id = Date.now();
    clientes.push({ id, nome, senha, moedas: Number(moedas) });
    listarClientes();
});

document.getElementById('seletorForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const nome = document.getElementById('seletorNome').value;
    const ip = document.getElementById('seletorIP').value;

    const id = Date.now();
    seletores.push({ id, nome, ip });
    listarSeletores();
});

document.getElementById('transacaoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const remetente = document.getElementById('transacaoRemetente').value;
    const recebedor = document.getElementById('transacaoRecebedor').value;
    const valor = document.getElementById('transacaoValor').value;

    const id = Date.now();
    transacoes.push({ id, remetente, recebedor, valor: Number(valor), status: 'Pendente' });
    listarTransacoes();
});

function listarClientes() {
    const ul = document.getElementById('clientesList');
    ul.innerHTML = '';
    clientes.forEach(cliente => {
        const li = document.createElement('li');
        li.textContent = `ID: ${cliente.id}, Nome: ${cliente.nome}, Moedas: ${cliente.moedas}`;
        ul.appendChild(li);
    });
}

function listarSeletores() {
    const ul = document.getElementById('seletorList');
    ul.innerHTML = '';
    seletores.forEach(seletor => {
        const li = document.createElement('li');
        li.textContent = `ID: ${seletor.id}, Nome: ${seletor.nome}, IP: ${seletor.ip}`;
        ul.appendChild(li);
    });
}

function listarTransacoes() {
    const ul = document.getElementById('transacoesList');
    ul.innerHTML = '';
    transacoes.forEach(transacao => {
        const li = document.createElement('li');
        li.textContent = `ID: ${transacao.id}, Remetente: ${transacao.remetente}, Recebedor: ${transacao.recebedor}, Valor: ${transacao.valor}, Status: ${transacao.status}`;
        ul.appendChild(li);
    });
}

// Buscar cliente pelo ID
function buscarClientePorId(id) {
    return clientes.find(cliente => cliente.id === id);
}

// Editar cliente pelo ID
function editarClientePorId(id, moedas) {
    const cliente = buscarClientePorId(id);
    if (cliente) {
        cliente.moedas = moedas;
        listarClientes();
    } else {
        alert('Cliente não encontrado');
    }
}

// Apagar cliente pelo ID
function apagarClientePorId(id) {
    clientes = clientes.filter(cliente => cliente.id !== id);
    listarClientes();
}

// Buscar seletor pelo ID
function buscarSeletorPorId(id) {
    return seletores.find(seletor => seletor.id === id);
}

// Editar seletor pelo ID
function editarSeletorPorId(id, nome, ip) {
    const seletor = buscarSeletorPorId(id);
    if (seletor) {
        seletor.nome = nome;
        seletor.ip = ip;
        listarSeletores();
    } else {
        alert('Seletor não encontrado');
    }
}

// Apagar seletor pelo ID
function apagarSeletorPorId(id) {
    seletores = seletores.filter(seletor => seletor.id !== id);
    listarSeletores();
}

// Buscar transação pelo ID
function buscarTransacaoPorId(id) {
    return transacoes.find(transacao => transacao.id === id);
}

// Editar transação pelo ID
function editarTransacaoPorId(id, status) {
    const transacao = buscarTransacaoPorId(id);
    if (transacao) {
        transacao.status = status;
        listarTransacoes();
    } else {
        alert('Transação não encontrada');
    }
}

// Validar transação (exemplo simplificado)
function validarTransacao(id) {
    const transacao = buscarTransacaoPorId(id);
    if (transacao) {
        transacao.status = 'Validada';
        listarTransacoes();
    } else {
        alert('Transação não encontrada');
    }
}

// Exemplo de como adicionar a busca, edição e exclusão à interface
document.getElementById('clientesList').addEventListener('click', function(e) {
    if (e.target && e.target.nodeName == "LI") {
        const id = parseInt(e.target.textContent.split(',')[0].split(': ')[1]);
        const cliente = buscarClientePorId(id);
        if (cliente) {
            const novasMoedas = prompt('Digite a nova quantidade de moedas:', cliente.moedas);
            if (novasMoedas !== null) {
                editarClientePorId(id, Number(novasMoedas));
            }
        }
    }
});

document.getElementById('seletorList').addEventListener('click', function(e) {
    if (e.target && e.target.nodeName == "LI") {
        const id = parseInt(e.target.textContent.split(',')[0].split(': ')[1]);
        const seletor = buscarSeletorPorId(id);
        if (seletor) {
            const novoNome = prompt('Digite o novo nome:', seletor.nome);
            const novoIp = prompt('Digite o novo IP:', seletor.ip);
            if (novoNome !== null && novoIp !== null) {
                editarSeletorPorId(id, novoNome, novoIp);
            }
        }
    }
});

document.getElementById('transacoesList').addEventListener('click', function(e) {
    if (e.target && e.target.nodeName == "LI") {
        const id = parseInt(e.target.textContent.split(',')[0].split(': ')[1]);
        const transacao = buscarTransacaoPorId(id);
        if (transacao) {
            const novoStatus = prompt('Digite o novo status:', transacao.status);
            if (novoStatus !== null) {
                editarTransacaoPorId(id, novoStatus);
            }
        }
    }
});