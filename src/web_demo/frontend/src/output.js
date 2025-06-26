import React from 'react';

function StyleOutput(props) {
    return (
        <div>
            <h3><b>OUTPUT:</b></h3>
            <br />
            {props.output_data && props.output_data.output_text ? (
                <>
                    {props.output_data.output_text}
                    <br /><br />
                    <b>BLEU:</b> {props.output_data.bleu_score}
                    <br />
                    <b>ROUGE:</b> {props.output_data.rouge_score}
                    <br />
                    <b>METEOR:</b> {props.output_data.meteor_score}
                    <br />
                    <b>BERT SCORE:</b> {props.output_data.bertscore}
                </>
            ) : (
                <div>Loading...</div>
            )}
        </div>
    );
}

export default StyleOutput;
