import React from 'react';
import './Message.css';


const ExampleSnippet = ({ exampleText, exampleLanguage }) => {
    return (
        <div style={{ margin: '2vh 0vh 2vh' }}>
            <div className='ExampleHeader'>{exampleLanguage}</div>
            <div className='ExampleSnippet'>
                {exampleText}
            </div>
        </div>
    )
}

export default ExampleSnippet;