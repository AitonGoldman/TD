import { NgModule } from '@angular/core';
import { PssPageComponent } from './pss-page/pss-page';
import { CustomHeaderComponent } from './custom-header/custom-header';
import { CreateEditEntityComponent } from './create-edit-entity/create-edit-entity';
import { EventComponent } from './event/event';
import { TournamentComponent } from './tournament/tournament';
import { TournamentMachinesComponent } from './tournament-machines/tournament-machines';
import { ExpandableComponent } from './expandable/expandable';
import { AddUserComponent } from './add-user/add-user';
@NgModule({
	declarations: [
            PssPageComponent,    
            CustomHeaderComponent,
            CreateEditEntityComponent,
            EventComponent,
            TournamentComponent,
            TournamentMachinesComponent,
            ExpandableComponent,
    AddUserComponent],
    imports: [],
    exports: [
        PssPageComponent,
        CustomHeaderComponent,
        CreateEditEntityComponent,
        EventComponent,
        TournamentComponent,
        TournamentMachinesComponent,
        ExpandableComponent,
    AddUserComponent]
})
export class ComponentsModule {}
