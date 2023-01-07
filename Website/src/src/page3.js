import { Col, Row, Container, Card } from "react-bootstrap";
import './styles/page3.css';

function Three(){
    return(
        <div className="con" >
            <div className="porto">
                {/* <img className='vector-top' src={require('./img/Vector 3.png')}></img> */}
                <div sm={4} className="Oapp">
                    <div className="bgBlur">
                        <div className="conDesk">
                        <div>
                            <h2 style={{color:"#E08839",textAlign:'center'}} className='header2'>OUR APPLICATION</h2>
                        </div>
                        <div className="conDesk">
                            <p style={{textAlign:'justify', color:"#ffff"}}>Aplikasi Yourney adalah aplikasi yang dapat memberikan minat pengguna aplikasi dengan memprediksikan minat mereka dengan menggunakan teknologi Artificial Intelligence, sesuai dengan tagline kami yaitu “Make Your Journey Yours” kami berusaha memberikan rekomendasi destinasi wisata yang sesuai dengan minat pengguna dengan adanya unsur fleksibilitas pengguna dalam menentukan dan menyesuaikan rekomendasi wisata yang telah diberikan. </p>
                        </div >
                        <div className="conPs">
                            <img className='ps' src={require('./img/foot.png')}></img>
                            </div>
                    </div>
                    </div>
                </div>
                <div sm={8} className="layoutImg">
                    <div className="marginR">
                        <img src={require('./img/ph1.png')} className='pImg'></img>
                        <img src={require('./img/ph2.png')} className='pImg1'></img>
                    </div>
                    <div className="marginR">
                        <img src={require('./img/ph3.png')} className='pImg2'></img>
                        <img src={require('./img/ph4.png')} className='pImg3'></img>
                    </div>
                </div>
                {/* <img className='vector-bottom' src={require('./img/Vector 4.png')}></img> */}
            </div>
        </div>
    );
}

export default Three;