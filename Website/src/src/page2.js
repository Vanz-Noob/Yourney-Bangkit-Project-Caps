import './styles/page2.css';


function Two(){
    return(
        <body className='body2' id="portofolio">
            <div className='conContent'>
                <div className='banner'>
                    <div className='obj'></div>
                    <div className='obj1'></div>
                    <div className='tBanner'>
                        <h1 className='hBanner'>TOP 15</h1>
                        <p className='dBanner'>PRODUCT CAPSTONE BANGKIT 2022</p>
                    </div>
                        
                </div>
                <div className='sponsor'>
                    <div className='sItem'>
                        <div className='sText'>
                            <span>Funded by :</span>
                        </div>
                        <div className='sImgCon'>
                            <img src={require('./img/kemendikbud.png')} className='sImg'/>
                            <img src={require('./img/google1.png')} className='sImg'/>

                        </div>
                    </div>
                    <div className='sItem'>
                        <div className='sText'>
                            <span>Supported by :</span>
                        </div>
                        <div className='sImgCon'>
                            <img src={require('./img/logo_trans.png')} className='sImg'/>
                            <img src={require('./img/bangkit.png')} className='sImg'/>

                        </div>
                    </div>
                </div>
            </div>
        </body>
    )
}


export default Two;