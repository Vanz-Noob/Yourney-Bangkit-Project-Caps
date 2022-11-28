import './styles/page1.css';
import { Navbar,Button,Container,Nav, NavbarBrand } from 'react-bootstrap';
import { IoIosArrowDown } from "react-icons/io";
import { useEffect, useState, useRef } from 'react';

function One() {
  const[nav,setNav] = useState('')
  
  const toggleVisible = () => {
    const scrolled = document.documentElement.scrollTop;
    if (scrolled > 500){
      setNav('dark')
    } 
    else if (scrolled <= 500){
      setNav('')
    }
  };

  console.log(nav)

  const scrollToTop = () =>{
    window.scrollTo({
      top: 0, 
      behavior: 'auto'

    });
  };


  window.addEventListener('scroll', toggleVisible);
  return (
    <div className='App' onScroll={scrollToTop} >

    {/* NAVBAR */}
    <Navbar variant='dark' expand="lg" fixed='top' bg={nav} className='trans'>
      <Container>
        <Navbar.Brand href="#home">
          <img src={require("./img/logo.png")} height="60"></img>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" style={{justifyContent:'flex-end'}}>
          <Nav>
            <Nav.Link href="#team">About Us</Nav.Link>
            <Nav.Link href="#portofolio">Portofolio</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
        
    {/* Body 1 */} 
      <div className='body' id='home'>
        
        <div className='conTitle'>
          <span className='tag' >MAKE IT JOURNEY IS YOURS</span>
          {/* <Button variant='success' size='lg' href='#produk'>GET STARTED</Button> */}
        </div>
        <a className='arw' href='#produk'>
          <IoIosArrowDown color='#E08839' size={100} className='btmArrow'/>
        </a>
      </div>
    
    </div>
  );
}

export default One;
