import { Col, Row, Container, Card } from "react-bootstrap";
import './styles/page3.css';

function Three(){
    return(
        <div className="con" id="portofolio">
            <div className="porto">
                <div sm={4} className="Oapp">
                    <div>
                        <h2 style={{color:"#ffff"}}>OUR APPLICATION</h2>
                    </div>
                    <div>
                        <p style={{textAlign:'justify', color:"#ffff"}}>Aplikasi Yourney adalah aplikasi yang dapat memberikan minat pengguna aplikasi dengan memprediksikan minat mereka dengan menggunakan teknologi Artificial Intelligence, sesuai dengan tagline kami yaitu “Make Your Journey Yours” kami berusaha memberikan rekomendasi destinasi wisata yang sesuai dengan minat pengguna dengan adanya unsur fleksibilitas pengguna dalam menentukan dan menyesuaikan rekomendasi wisata yang telah diberikan. </p>
                    </div>
                    <div>
                        <img className='ps' src={require('./img/foot.png')}></img>
                    </div>
                </div>
                <div sm={8} className="layoutImg">
                    <div style={{marginRight:10}}>
                        <img src={require('./img/ph1.png')} className='pImg'></img>
                        <img src={require('./img/ph2.png')} className='pImg1'></img>
                    </div>
                    <div>
                        <img src={require('./img/ph3.png')} className='pImg2'></img>
                        <img src={require('./img/ph4.png')} className='pImg3'></img>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Three;