import React from 'react';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';


const MessageContent = ({ message, isReviewed, handlePlaySpeak, handleThumbsUp, handleThumbsDown }) => {
    return (
        <span>
            {message.text}
            {message.examples.map((example, index) => {
                return (
                    <div style={{ margin: '2vh 0vh 2vh' }} key={index}>
                        <div className='ExampleHeader'>{message.languages[index]}</div>
                        <div className='ExampleSnippet'>
                            {example}
                        </div>
                    </div>
                )
            })}
            {message.actor === 'Bot' && (
                <Stack
                    direction={'row'}
                    spacing={1}
                >
                    <IconButton
                        size='small'
                        aria-label="speak"
                        onClick={() => handlePlaySpeak(message.text)}
                    ><VolumeUpIcon fontSize="inherit"/></IconButton>
                    {!isReviewed && (
                        <>
                            <IconButton
                                size='small'
                                aria-label="like"
                                onClick={handleThumbsUp}
                            ><ThumbUpIcon fontSize="inherit"/></IconButton>
                            <IconButton
                                size='small'
                                aria-label="dislike"
                                onClick={handleThumbsDown}
                            ><ThumbDownIcon fontSize="inherit"/></IconButton>
                        </>
                    )}
                </Stack>
            )}
        </span>
    );
}

export default MessageContent;