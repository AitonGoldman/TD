import { ViewChild, Component } from '@angular/core';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { IonicPage } from 'ionic-angular';


/**
 * Generated class for the PlayerInfoPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'PlayerInfo/:eventId'
})
@Component({
  selector: 'page-player-info',
  templateUrl: 'player-info.html',
})
export class PlayerInfoPage extends AutoCompleteComponent {
    loading:boolean=false;
    ticketCounts:any=null;
    selectedPlayer:any=null;    
    player_id_for_event:number=null;
    playerLoadStatus:string='notStarted';
    @ViewChild('searchbar')  searchbar: any;    
    singleUser:any=null;
    displayExistingUserNotFound:boolean = false;
    
    
    ionViewWillLoad() {
      console.log('ionViewDidLoad PlayerInfoPage');
      //this.autoCompleteProvider.setPlayerSearchType("allPlayers",
      //                                              this.generateLoadingFunction());      
        this.events.subscribe('autocomplete:done', (autocompleteInfo, time) => {
            // user and time are the same arguments passed in `events.publish(user, time)`
            this.loading=false;
            if(autocompleteInfo.state=='DONE' && autocompleteInfo.type=='SEARCH_SINGLE'){
                console.log(autocompleteInfo);
                if(autocompleteInfo.data==null){
                    return;
                }
                this['selectedPlayer']=autocompleteInfo.data.data;
                this['ticketCounts']=this.generateListFromObj(this['selectedPlayer'].tournament_counts);                
                
            }
            if(autocompleteInfo.state=='DONE' && autocompleteInfo.type=='SEARCH_LIST'){
                console.log(autocompleteInfo);
                if(autocompleteInfo.data.data.length==0){
                    let toast = this.toastCtrl.create({
                        message:  "No Such Player in Event -- ",
                        duration: 99000,
                        position: 'top',
                        showCloseButton: true,
                        closeButtonText: " ",
                        cssClass: "dangerToast"
                    });
                    toast.present();                                    
                }
                
            }            
        });
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                         null,
                                                         this.generatePlayerLoadingFunction(),
                                                         this.eventId);      
      
      let player_id_for_event = this.navParams.get('player_id_for_event');
      if(player_id_for_event==null){          
          return;            
      }      
      this.player_id_for_event=player_id_for_event
      //this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
      //    .subscribe(this.generateGetEventPlayerProcessor())                                                  
        
  }
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;
        this.ticketCounts=null;
        //this.selectedPlayer={player_full_name:null,player_id_for_event:null,first_name:null,last_name:null};
    }
    
    onInput(event){        
        console.log('in onInput...')
        console.log(event);
        this.loading=true;                
    }

    onItemsShown(){
        console.log('in onItemsShown');
    }
        
        
    clearValues(){
        this.selectedPlayer={};
        //this.eventPlayer={};
        //this.player_id_for_event=null;        
    }

}