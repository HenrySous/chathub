const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);

const io = new Server(server, {
    cors: {
        origin: "*"
    }
});

app.use(express.static("public"));

let historico = [];

io.on("connection", (socket) => {
    console.log("Usuário conectado");

    socket.on("entrar", (nome) => {
        socket.nome = nome;

        io.emit("mensagem", {
            sistema: `>>> ${nome} entrou no chat`
        });

        historico.forEach(msg => {
            socket.emit("mensagem", msg);
        });
    });

    socket.on("mensagem", (texto) => {
        const msg = {
            nome: socket.nome,
            texto,
            hora: new Date().toLocaleTimeString()
        };

        historico.push(msg);

        if (historico.length > 100) {
            historico.shift();
        }

        io.emit("mensagem", msg);
    });

    socket.on("disconnect", () => {
        if (socket.nome) {
            io.emit("mensagem", {
                sistema: `<<< ${socket.nome} saiu`
            });
        }

        console.log("Usuário desconectado");
    });
});

server.listen(3000, "0.0.0.0", () => {
    console.log("Servidor rodando:");
    console.log("http://localhost:3000");
});
