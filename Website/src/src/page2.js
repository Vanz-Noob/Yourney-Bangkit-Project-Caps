import './styles/page2.css';
import { Row,Col,Card } from 'react-bootstrap';


function Two(){
    return(
        <div className='pg2' id='produk'>
            <div className='bg2'> 
                <div className='con-content'>
                    <div className='cardContent'>
                        <div className='bestCont'>
                            <div className='cBody' >
                                <h1 className='cTitle' >TOP 50</h1>
                                <text className='text' >PRODUCT CAPSTONE BANGKIT 2022</text>
                            </div>
                        </div>
                    </div>
                        <div className='Row'>
                            <div className='Col'>
                                <div className='item'>
                                    <img src={require('./img/kemendikbud.png')} style={{width:'135px',height:'117px'}}></img>
                                    <span style={{width:'50%'}}>Funded by kemendikbudristek</span>
                                </div>
                                <div className='item'>
                                    <img src={require('./img/trans 1.png')} style={{width:'135px',height:'117px'}}></img>
                                    <span style={{width:'50%'}}>Support by Bandung Techo Park</span>
                                </div>
                            </div>
                            <div className='Col'>
                                <div className='item'>
                                    <img src={require('./img/google.png')} style={{width:'135px',height:'117px'}} className='hov'></img>
                                    <span style={{width:'50%'}}>Funded by Google Indonesia</span>
                                </div>
                                <div className='item'>
                                    <img src={require('./img/bangkit.png')} style={{width:'100px',height:'100px'}}></img>
                                    <span style={{width:'50%'}}>Support by Google Bangkit Academy</span>
                                </div>
                            </div>
                        </div>
                </div>
            </div>
        </div>
    )
}


export default Two;