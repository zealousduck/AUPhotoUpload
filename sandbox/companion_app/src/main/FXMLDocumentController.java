/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package main;

import java.net.URL;
import java.util.ResourceBundle;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;


/**
 *
 * @author Trenton
 */
public class FXMLDocumentController implements Initializable {
    
    @FXML
    public Button button1;
    public Button button2;
    
    @FXML
    public void button1Click(ActionEvent event) {
        System.out.println("You clicked button 1!");
        
    }
    
    @FXML
    public void button2Click(ActionEvent event) {
        System.out.println("You clicked button 2!");
        
    }
    
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        // TODO
    }    
    
}
