import './styles/page4.css';

function Four(){
    return(
        <>
              <body className='body4' id='team'>
                <h1>Meet Our Team</h1>
                <div className='layer1'>
                    <img src={require('./img/image 1.png')}></img>
                    <img src={require('./img/image 5.png')}></img>
                </div>
                <div className='layer2'>
                    <img src={require('./img/daf.png')}></img>
                    <img src={require('./img/co.png')}></img>
                </div>
                <div className='center'>
                    <img src={require('./img/ren.png')}></img>
                </div>
                <div className='layer4'>
                    <img src={require('./img/image 2.png')}></img>
                    <img src={require('./img/image 3.png')}></img>
                </div>
            </body>
        
        </>
    )
}

export default Four;