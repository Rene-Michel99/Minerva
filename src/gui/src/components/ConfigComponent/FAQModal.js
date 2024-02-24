import React from "react";
import CloseIcon from '@mui/icons-material/Close';
import { IconButton } from "@mui/material";
import './Config.css';


const FAQModal = ({
    handleClose
}) => {

    return (
        <div className="FAQModal">
            <div className="ModalHeader">
                <h3>Ajuda e FAQs</h3>
                <IconButton onClick={handleClose}><CloseIcon color="primary"/></IconButton>
            </div>
            <hr/>
            <br/>
            <div>
                <h3>Pergunta 1: Como posso começar uma conversa com o chatbot?</h3>
                <p>Resposta: Você pode iniciar uma conversa com o chatbot digitando uma mensagem na caixa de texto na parte inferior da janela de chat e pressionando Enter. O chatbot responderá assim que receber sua mensagem.</p>

                <h3>Pergunta 2: O chatbot oferece suporte a quais idiomas?</h3>
                <p>Resposta: Atualmente, o chatbot oferece suporte aos seguintes idiomas: português. Você pode selecionar seu idioma preferido na configuração do chatbot.</p>

                <h3>Pergunta 3: Como posso alterar minhas configurações de notificação?</h3>
                <p>Resposta: Para alterar suas configurações de notificação, clique no ícone de configurações na barra lateral e selecione a opção "Configurações de Notificação". Você poderá ativar ou desativar as notificações e personalizar suas preferências de notificação.</p>

                <h3>Pergunta 4: Existe uma lista de comandos que posso usar com o chatbot?</h3>
                <p>Resposta: Sim, você pode digitar "ajuda" ou "comandos" para receber uma lista de comandos disponíveis que você pode usar com o chatbot. Você também pode acessar a página de Ajuda na barra lateral para obter mais informações sobre os comandos disponíveis.</p>

                <h3>Pergunta 5: Como posso fornecer feedback sobre o chatbot?</h3>
                <p>Resposta: Adoraríamos ouvir sua opinião! Você pode fornecer feedback sobre o chatbot clicando no ícone de feedback na barra lateral e preenchendo o formulário de feedback. Seu feedback é importante para nos ajudar a melhorar o chatbot.</p>
            </div>
        </div>
    )
}

export default FAQModal;