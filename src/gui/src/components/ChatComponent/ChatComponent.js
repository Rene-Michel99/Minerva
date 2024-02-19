import React, { useState, useRef, useEffect } from 'react';
import TextToSpeech from './TTS.js';
import './ChatComponent.css';
import LoadingMessage from './Message/LoadingMessage.js';
import MessageComponent from './Message/MessageComponent.js';
import ErrorBar from './ErrorBar.js';


const ChatComponent = ({voice, pitch, volume, rate, isSpeaking, darkTheme, autoSpeak, handleSpeaking}) => {
    const [messages, setMessages] = useState([{
        id: 9,
        actor: "Bot",
        text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        examples: ["import tensorflow as tf\n\nx = 10\ndef sum(a,b):\n\treturn a + b"],
        languages: ["Python"]
    }]);
    const [processing, setProcessing] = useState(false);
    const [waitingMessage, setWaitingMessage] = useState(false);
    const [openErrorBar, setopenErrorBar] = useState(false);
    const [errorMessage, setErrorMessage] = useState('error');
    const [utterance, setUtterance] = useState(null);
    const messagesEndRef = useRef(null);

    const handleProcessing = (value) => {
        setProcessing(value);
    }

    const handleWaitingMessage = (value) => {
        setWaitingMessage(value)
    }

    const handleNewMessage = (actor, data) => {
        setMessages((previousMessages) => [
            ...previousMessages,
            {
                id: data.id,
                actor: actor,
                text: data.text,
                examples: data.examples,
                languages: data.languages
            }
        ]);
    }
    
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    const handleOpenErrorBar = (errorMessage) => {
        setopenErrorBar(true);
        setErrorMessage(errorMessage);
    }

    const playAudio = async (synth, responseText) => {
        utterance.text = responseText;
        utterance.voice = voice;
        utterance.pitch = pitch;
        utterance.rate = rate;
        utterance.volume = volume;
    
        synth.speak(utterance);
    }

    const handlePlaySpeak = async (responseText) => {
        const synth = window.speechSynthesis;
    
        await playAudio(synth, responseText);
    };

    useEffect(() => {
        const synth = window.speechSynthesis;
    
        const u = new SpeechSynthesisUtterance('');
        u.onstart = () => {
            handleSpeaking(true);
        }
        u.onend = () => {
            handleSpeaking(false);
            handleProcessing(false);
        };

        setUtterance(u);
        scrollToBottom();
        return () => {
            synth.cancel();
        };
    }, [messages]);

    return (
        <div className="Chat">
            <div className='Interactions'>
                {messages.map((message) => {
                    return (
                        <MessageComponent
                            key={message.id}
                            message={message}
                            darkTheme={darkTheme}
                            handleOpenErrorBar={handleOpenErrorBar}
                            handlePlaySpeak={handlePlaySpeak}
                        />
                    )
                })}
                {waitingMessage && (
                    <LoadingMessage darkTheme={darkTheme}/>
                )}
                <div ref={messagesEndRef} />
            </div>
            <TextToSpeech
                processing={processing}
                autoSpeak={autoSpeak}
                darkTheme={darkTheme}
                handlePlaySpeak={handlePlaySpeak}
                handleNewMessage={handleNewMessage}
                handleProcessing={handleProcessing}
                handleWaitingMessage={handleWaitingMessage}
                handleOpenErrorBar={handleOpenErrorBar}
            />
            <ErrorBar
                errorMessage={errorMessage}
                openErrorBar={openErrorBar}
                setopenErrorBar={setopenErrorBar}
            />
        </div>
    );
}

export default ChatComponent;