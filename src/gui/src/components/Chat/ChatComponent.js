import React, { useState, useRef, useEffect } from 'react';
import TextToSpeech from './TTS.js';
import './ChatComponent.css';
import LoadingMessage from '../Message/LoadingMessage.js';
import MessageComponent from '../Message/MessageComponent.js';
import ErrorBar from './ErrorBar.js';


const ChatComponent = ({voice, pitch, volume, rate, isSpeaking, autoSpeak, handleSpeaking}) => {
    const [inputText, setInputText] = useState('');
    const [messages, setMessages] = useState([]);
    const [processing, setProcessing] = useState(false);
    const [waitingMessage, setWaitingMessage] = useState(false);
    const [openErrorBar, setopenErrorBar] = useState(false);
    const [errorMessage, setErrorMessage] = useState('error');
    const [utterance, setUtterance] = useState(null);
    const messagesEndRef = useRef(null)

    const handleProcessing = (value) => {
        setProcessing(value);
    }

    const handleWaitingMessage = (value) => {
        setWaitingMessage(value)
    }

    const handleNewMessage = (actor, text, id) => {
        setMessages((previousMessages) => [
            ...previousMessages,
            {
                id: id,
                actor: actor,
                text: text
            }
        ]);
    }

    const handleInputChange = (event) => {
        if (!isSpeaking) {
            setInputText(event.target.value);
        }
    };
    
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    const handleOpenErrorBar = (errorMessage) => {
        setopenErrorBar(true);
        setErrorMessage(errorMessage);
    }

    const handleNewUtterance = () => {
        const synth = window.speechSynthesis;
    
        const u = new SpeechSynthesisUtterance(inputText);
        u.onstart = () => {
        handleSpeaking(true);
        }
        u.onend = () => {
        console.log('Fala concluída');
        handleSpeaking(false);
        handleProcessing(false);
        };

        setUtterance(u);
        return () => {
            synth.cancel();
        };
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
        handleNewUtterance();
        scrollToBottom();
    }, [messages]);

    return (
        <div className="Chat">
            <div className='Interactions'>
                {messages.map((message) => {
                    return (
                        <MessageComponent
                            key={message.id}
                            message={message}
                            handleOpenErrorBar={handleOpenErrorBar}
                            handlePlaySpeak={handlePlaySpeak}
                        />
                    )
                })}
                {waitingMessage && (
                    <LoadingMessage />
                )}
                <div ref={messagesEndRef} />
            </div>
            <TextToSpeech
                text={inputText}
                processing={processing}
                autoSpeak={autoSpeak}
                handlePlaySpeak={handlePlaySpeak}
                handleInputChange={handleInputChange}
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