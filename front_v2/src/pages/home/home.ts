import { ViewChild, Component } from '@angular/core';
import { IonicPage, Tabs } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the HomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({    
    segment: 'HomePage/:eventId'
})
@Component({
  selector: 'page-home',
  templateUrl: 'home.html',
})
export class HomePage extends PssPageComponent{
    @ViewChild('myTabs') tabRef: Tabs;    

    ionViewDidLoad() {
        console.log('ionViewDidLoad HomePage');        
    }
}