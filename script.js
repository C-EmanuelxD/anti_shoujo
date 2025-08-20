

const botaoSubmit = document.getElementById('btn_submit');

if (botaoSubmit){
    botaoSubmit.addEventListener('click', handler_submit);
}else{
    console.log("Bot~çao n~çao encontradp");
}



async function handler_submit(event){
    event.preventDefault();
    event.stopPropagation();
    document.getElementById("infos_exibicao").innerHTML = "";
    const caixaTexto =  document.getElementById('text_mangas');
    const mangaNomes = caixaTexto.value;
    const lista_nomes = mangaNomes.split(/\r?\n/).filter(line => line.trim() !== '');

    console.log(lista_nomes);

    if (lista_nomes.length === 0) {
        console.log("Nenhum nome de mangá foi inserido.");
        return;
    }
    try{
        
        const mangaInfos = await manga_info(lista_nomes);
        for(let i = 0; i < mangaInfos.length; i++){
            let titulo = mangaInfos[i].titulo;
            let desc = mangaInfos[i].descricao;
            let capitulo = mangaInfos[i].capitulos;
            let img = mangaInfos[i].url_imagem;

            criar_info(img, titulo, desc, capitulo);
        }

    }catch (erro){
        console.error(erro);
        alert('erro!');
    }


}


async function manga_info(lista_nomes){
   const url = 'http://localhost:5000/receive'
    const config = {
        method :'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'lista': lista_nomes})
    }
    try{
        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error("Algum erro aconteceu na resposta!");
        }
        
        const dadosResposta = await response.json();

        console.log(dadosResposta);

        if (dadosResposta.createdItems == 0){
            alert("Nenhum não Shoujo encontrado!");
        }

        if (!dadosResposta || !dadosResposta.createdItems) {
            throw new Error("Resposta da API não contém 'createdItems'.");
        }
        return dadosResposta.createdItems;
    }catch (erro){
        console.error("Erro API" + erro);
        throw new Error("ERO DE API FODA");
    }
}

function criar_info(img, titulo, desc, caps){
    try{

        const allDiv = document.createElement('div'); //DIV COM TUDO
        const imgDiv = document.createElement('div'); //DIV DA IMAGEM A ESQUERDA
        const informacoesDiv = document.createElement('div'); //DIV DAS INFOS A DIREITA

        const mangaImg = document.createElement('img'); //LINK PARA O MANGA
        const informacoesTitulo = document.createElement('h1'); //TITULO DO MANGA
        const informacoesDesc = document.createElement('p'); //DESCRIÇÃO DO MANGA
        const qtdCap = document.createElement('p');

        informacoesTitulo.textContent = titulo; //ADICIONA TEXTO AO TITULO
        
        informacoesDesc.textContent = desc; //ADICIONA TEXTO A DESCRICAO
        qtdCap.textContent = 'Capitulos: ' + caps
        
        informacoesDesc.classList.add('paragrafo-infos');
        informacoesTitulo.classList.add('titulo-manga');
        allDiv.classList.add('dir-infos'); //PEGA A CLASSE CSS 'INFOS' E FAZ A DIV MAIOR USAR ELA
        mangaImg.classList.add('img');

        mangaImg.src = img
        mangaImg.alt = informacoesTitulo.textContent;


        imgDiv.appendChild(mangaImg);

        allDiv.appendChild(imgDiv);
        allDiv.appendChild(informacoesDiv);

        informacoesDiv.appendChild(informacoesTitulo);
        informacoesDiv.appendChild(informacoesDesc);
        informacoesDiv.appendChild(qtdCap);

        informacoesDiv.classList.add('infos');




        const infosDisplay = document.getElementById('infos_exibicao');
        
        infosDisplay.appendChild(allDiv);
    }catch (erro){
        console.error("O erro é no criar_info");
        throw new Error("Criar_Info ERROR!");
    }
}
