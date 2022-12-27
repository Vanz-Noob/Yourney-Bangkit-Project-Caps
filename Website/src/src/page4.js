import './styles/page4.css';
import { Modal, Button } from 'react-bootstrap';
import React,{ useState, useEffect } from 'react';
import {IoLogoLinkedin,IoLogoGithub} from "react-icons/io";


function Four(){
    const [show, setShow] = useState(false);
    const [name, setName] = useState('')
    const [link,setLink] = useState('')
    const [git,setGit] = useState('')
    const [url,setUrl] =useState()

    var personil =require('./Personil.json')

    const handleClose = () => setShow(false);
    const handleShow = () =>{
        setShow(true);
        setName(personil[0].Name)
        setUrl(require(`${personil[0].img}`))
        setLink(personil[0].linkedin)
        setGit(personil[0].github)

    } 
    const handleShow2 = () =>{
        setShow(true);
        setName(personil[1].Name)
        setUrl(require(`${personil[1].img}`))
        setLink(personil[1].linkedin)
        setGit(personil[1].github)
    } 
    const handleShow3 = () =>{
        setShow(true);
        setName(personil[2].Name)
        setUrl(require(`${personil[2].img}`))
        setLink(personil[2].linkedin)
        setGit(personil[2].github)
    } 
    const handleShow4 = () =>{
        setShow(true);
        setName(personil[3].Name)
        setUrl(require(`${personil[3].img}`))
        setLink(personil[3].linkedin)
        setGit(personil[3].github)
    } 
    const handleShow5 = () =>{
        setShow(true);
        setName(personil[4].Name)
        setUrl(require(`${personil[4].img}`))
        setLink(personil[4].linkedin)
        setGit(personil[4].github)
    } 
    const handleShow6 = () =>{
        setShow(true);
        setName(personil[5].Name)
        setUrl(require(`${personil[5].img}`))
        setLink(personil[5].linkedin)
        setGit(personil[5].github)
    } 



    return(
        <body className='four' >
        <Modal show={show} onHide={handleClose} size='lg' centered='true' >
        <Modal.Header closeButton>
        </Modal.Header>
        <Modal.Body >
            <div className='bModal'>
                <img className='iModal' src={url}></img>
                <span className='nModal'>{name}</span>
            </div>
        </Modal.Body>
        <Modal.Footer>
            <a href={link} target="_blank"><IoLogoLinkedin size={50}/></a>
            <a href={git} target="_blank"><IoLogoGithub size={50}/></a>
        </Modal.Footer>
      </Modal>
            <div className='conTeam'>
                {/* ML */}
                <div className='conImg'>
                    <span className='titleT'>Machine Learning Team</span>
                    <div className='conImg1 ' >
                        <img className='img1 ' src={require('./img/Personil/BG White/alip.png')} onClick={handleShow} id='alif' ></img>
                    </div>
                    <div className='conImg1'>
                        <img className='img2 ' src={require('./img/Personil/BG White/aul.png')} onClick={handleShow2} id='aulia' ></img>
                    </div>
                    <div className='conImg1'>
                        <img className='img3 ' src={require('./img/Personil/BG White/man.png')} onClick={handleShow3} id='rochman'></img>
                    </div>
                </div>
                {/* MD */}
                {/* <div className='conImg'>
                    <span className='titleT'>Mobile Developer Team</span>
                        <div className='hoverName1'>
                        </div>
                    <img className='img4' src={require('./img/Personil/alif.jpeg')}></img>
                </div> */}
                {/* WD */}
                <div className='conImg'>
                    <span className='titleT'>Web Developer Team</span>
                    <img className='img5' src={require('./img/Personil/BG White/Dafa.png')} onClick={handleShow4}></img>
                </div>
                {/* CC */}
                <div className='conImg'>
                    <span className='titleT'>Cloud Computing Team</span>
                    <div className='conImg2'>
                        <img className='img6' src={require('./img/Personil/BG White/ginjal.png')} onClick={handleShow5}></img>
                    </div>
                    <div className='conImg2'>
                        <img className='img7' src={require('./img/Personil/BG White/coco.png')} onClick={handleShow6}></img>
                    </div>
                </div>
            </div>

        

        </body>
    )
}

export default Four;