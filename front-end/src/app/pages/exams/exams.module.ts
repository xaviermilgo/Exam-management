import { NgModule } from '@angular/core';
import { ThemeModule } from '../../@theme/theme.module';
import { ExamsComponent } from './exams.component';
import { EditTableComponent } from './edit-table/edit-table.component';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { SmartTableService } from '../../@core/data/smart-table.service';

@NgModule({
  imports: [
    ThemeModule,
    Ng2SmartTableModule
  ],
  declarations: [
    ExamsComponent,
    EditTableComponent,
  ],
  providers: [
    SmartTableService
  ],
})
export class ExamsModule { }

