import React from "react";
import { IoMail } from "react-icons/io5";
import { TiSocialInstagram } from "react-icons/ti";
import { FaLinkedinIn } from "react-icons/fa";
import "./styles.css";

function Footer() {
  return (
    <div
      style={{ height: "12rem", backgroundColor: "#062e28" }}
      className="Footer"
      id="Contact"
    >
      <p5>Find Us :</p5>
      <div className="Ficons">
        <a href="mailto: yourneyteam.id@gmail.com" target="_blank">
          <IoMail size={40} />
        </a>
        <a href="https://www.instagram.com/yourney.project/" target="_blank">
          <TiSocialInstagram size={40} />
        </a>
        <a
          href="https://www.linkedin.com/in/yourney-project-295325250"
          target="_blank"
        >
          <FaLinkedinIn size={40} />
        </a>
      </div>
      <p5>&copy; 2021-2022 Yourney</p5>
    </div>
  );
}

export default Footer;
