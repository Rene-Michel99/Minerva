import React from 'react';
import LinearProgress from '@mui/material/LinearProgress';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import MinervaIcon from '../../images/icon.jpeg';
import './Message.css';


const LoadingMessage = () => {
    return (
        <Box className='LoadingMessage scale-up-center'>
            <div className='GhostMessage'>
                <Avatar alt="Minerva" src={MinervaIcon} sx={{ width: 56, height: 56 }} />
                <LinearProgress className='LinearProgressCenter'/>
            </div>
        </Box>
    );
}

export default LoadingMessage;