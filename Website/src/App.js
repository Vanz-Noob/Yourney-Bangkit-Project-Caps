import One from "./src/page1";
import Two from "./src/page2";
import Three from "./src/page3";
import {FaCircle} from "react-icons/fa";
import './App.css';
import Four from "./src/page4";
import Five from "./src/page5";
import Footer from "./src/footer";
import { useState } from "react";


function App(){
    const[dot,setDot] = useState('white')
    // let team = document.getElementById("team");
    // let home = document.getElementById("home");
    // console.log('test',team.id)


    return(
        <body >
             {/* <div className="dotNavigation">
            <FaCircle color="orange"/>
            <FaCircle color={dot}/>
            <FaCircle color={dot}/>
            <FaCircle color={dot}/>
        </div> */}
        <One/>
        <Two/>
        <Three/>
        <Four/>
        {/* <Five/> */}
       <Footer/>
       

        </body>
        
    )
}

export default App;