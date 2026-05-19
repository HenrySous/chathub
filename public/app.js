const socket = io();

const nome = prompt("Seu nome?") || "Anônimo";

socket.emit("entrar", nome);

const mensagens = document.getElementById("mensagens");

socket.on("mensagem", (data) => {

    const div = document.createElement("div");

    div.classList.add("msg");

    if (data.sistema) {
        div.classList.add("sistema");
        div.innerText = data.sistema;
    } else {
        div.innerText =
            `[${data.hora}] ${data.nome}: ${data.texto}`;
    }

    mensagens.appendChild(div);

    mensagens.scrollTop = mensagens.scrollHeight;
});

function enviar() {
    const input = document.getElementById("texto");

    if (!input.value.trim()) return;

    socket.emit("mensagem", input.value);

    input.value = "";
}

document
.getElementById("texto")
.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        enviar();
    }
});
