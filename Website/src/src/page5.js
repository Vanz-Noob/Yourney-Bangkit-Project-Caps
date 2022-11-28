import { Button, Container, Form } from 'react-bootstrap';
import './styles/page5.css';

function Five(){
    return(
        <body className='body5'>
            <h1 style={{color:'#fff'}}>CONTACT US</h1>
            <Container>
                <Form className='form'>
                    <Form.Group className="mb-3">
                        <Form.Control placeholder='Name'></Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Control type='email' placeholder='Email'></Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Control type='number' placeholder='Phone'></Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-3">
                         <Form.Control placeholder='Text' as="textarea" rows={3}></Form.Control>
                    </Form.Group>
                    <Button style={{backgroundColor:'#00A58F'}}>Send</Button>
                </Form>
            </Container>
        </body>
    )
}

export default Five;