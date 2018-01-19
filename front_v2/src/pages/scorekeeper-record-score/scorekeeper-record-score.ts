import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

/**
 * Generated class for the ScorekeeperRecordScorePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment: 'ScorekeeperRecordScore/:eventId/:tournamentId/:tournamentMachineId'
})
@Component({
  selector: 'page-scorekeeper-record-score',
  templateUrl: 'scorekeeper-record-score.html',
})
export class ScorekeeperRecordScorePage extends PssPageComponent {
    tournamentId:any=null;
    tournamentMachine:any=null;
    tournamentMachineId:any=null;
    score:any=null;
    player_id_for_event:any=null;

    generateSubmitScoreProcessor(successSummary){
        return (result) => {
            if(result == null){
                return;
            }
            // console.log('in generateAddEventPlayerProcessor')
            console.log('in genrateSubmitScoreProcessor')
            console.log(result)
            let tournamentMachine=result.data;
            let successButtons=[];            
            
            let recordScoreSuccessButtons=['RE_ADD','RE_QUEUE','DEAL_WITH_PERSON_IN_QUEUE', 'DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER','GO_HOME']
            if(result.tournament_counts==0){
                recordScoreSuccessButtons=recordScoreSuccessButtons.filter((buttonLabel)=>{
                    if(buttonLabel=="RE_ADD" || buttonLabel=="RE_QUEUE" || buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER"){
                        return false;
                    } else {
                        return true;
                    }
                })
            }
            if(tournamentMachine.queues[0].player==null){
                recordScoreSuccessButtons=recordScoreSuccessButtons.filter((buttonLabel)=>{
                    if(buttonLabel=="RE_QUEUE" || buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE"|| buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER"){
                        return false;
                    } else {
                        return true;
                    }
                })
            }
            if(tournamentMachine.queues[0].player!=null){
                recordScoreSuccessButtons=recordScoreSuccessButtons.filter((buttonLabel)=>{
                    if(buttonLabel=="RE_ADD" || buttonLabel=="GO_HOME"){
                        return false;
                    }
                    if(result.tournament_counts==0){                        
                        if(buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER"){
                            return false;
                        }                         
                    } else {
                        if(buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE"){
                            return false;
                        }                         
                    }                    
                    return true;
                })
            }
            
            this.navCtrl.push("RecordScoreSuccessPage",            
                               this.buildNavParams({'successSummary':successSummary,
                                                    'successButtons':[],
                                                    'recordScoreSuccessButtons':recordScoreSuccessButtons,
                                                    'player':this.tournamentMachine.player,
                                                    'tournamentMachine':tournamentMachine,
                                                    'tournamentId':this.tournamentId}));
        };
    }

    voidTicket(){
        let actionSheet = this.actionSheetCtrl.create({
            title: 'Are you SURE you want to VOID the ticket?',
            buttons: [
                {
                text: 'VOID',
                role: 'destructive',
                handler: () => {
                    //this.onRemoveConfirmed(machine);
                    this.onVoid();
                    console.log('Destructive clicked');
                }
            },
                {
                text: 'Cancel',
                role: 'cancel',
                handler: () => {
                    console.log('Cancel clicked');
                }
            }
            ]
        });
        actionSheet.present();                
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad ScorekeeperRecordScorePage');
        this.tournamentId=this.navParams.get('tournamentId');
        this.tournamentMachineId=this.navParams.get('tournamentMachineId');
        this.tournamentMachine=this.navParams.get('tournamentMachine');
        if(this.tournamentMachine.player!=null && this.tournamentMachine.player.events != null){
            console.log('logging eventInfo');
            this.player_id_for_event = this.tournamentMachine.player.events.filter((eventInfo)=>{
                if(eventInfo.event_id==this.eventId){
                    return true
                }
            })[0].player_id_for_event;
        }
        console.log(this.tournamentMachine);
    }
    insertCommas(event){
        console.log('hi there');
        this.score = this.score.replace(/\,/g,'').replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
    }
    onVoid(){
        let success_title_string='Ticket Voided!';
        let success_line_one_string='Ticket for '+this.tournamentMachine.player.player_full_name + " has been voided on "+this.tournamentMachine.tournament_machine_name;        
            
        let successSummary = new SuccessSummary(success_title_string,success_line_one_string, null);            

        this.pssApi.voidTicket({tournament_id:this.tournamentId,tournament_machine_id:this.tournamentMachineId,player_id:this.tournamentMachine.player_id },this.eventId)            
            .subscribe(this.generateSubmitScoreProcessor(successSummary))        
    }
    
    onSubmit(){
        let success_title_string='Score recorded!';
        let success_line_one_string=this.tournamentMachine.player.player_full_name + " on machine "+this.tournamentMachine.tournament_machine_name;
        let success_line_two_string='Score of '+this.score+'.';
            
        let successSummary = new SuccessSummary(success_title_string,success_line_one_string, success_line_two_string);            

        this.pssApi.submitScore({tournament_id:this.tournamentId,tournament_machine_id:this.tournamentMachineId,player_id:this.tournamentMachine.player_id, action:'record_score',score:this.score.replace(new RegExp(',', 'g'), "")},this.eventId)            
            .subscribe(this.generateSubmitScoreProcessor(successSummary))        
    }
}
