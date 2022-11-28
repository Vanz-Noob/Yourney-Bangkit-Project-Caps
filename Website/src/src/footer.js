import './styles/footer.css'
import {IoLogoInstagram, IoLogoLinkedin, IoLogoWhatsapp, IoIosPin} from "react-icons/io";


function Footer(){
    return(
        <body className='foot'>
            <div className='footer'>
                <IoLogoWhatsapp color='white' size={20}/>
                <a href='https://www.instagram.com/yourney.project/'><IoLogoInstagram color='white' size={23} /></a>
                <IoLogoLinkedin color='white' size={20}/>
                <IoIosPin color='white' size={20}/>
            </div>
        </body>
    )
}

export default Footer;