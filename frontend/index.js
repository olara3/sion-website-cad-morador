const express = require('express');
const app = express();
const PORT = 3000;

// Rota Principal (Dashboard)
app.get('/sion', (req, res) => {
    res.send('<h1>Sion Condomínio - Dashboard OCI</h1><p>Node.js rodando na Oracle Cloud Ampere!</p>');
});

// Rota de Cadastro
app.get('/sion/cadastro', (req, res) => {
    res.send('<h1>Módulo de Cadastro - OCI</h1><p>Ambiente pronto para o formulário.</p>');
});

app.listen(PORT, '127.0.0.1', () => {
    console.log(`Frontend Node.js rodando em http://127.0.0.1:${PORT}`);
});
