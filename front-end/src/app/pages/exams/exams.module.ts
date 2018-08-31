import { NgModule } from '@angular/core';
import { ThemeModule } from '../../@theme/theme.module';
import { ExamsComponent } from './exams.component';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { NotificationsComponent } from './notifications/notifications.component';
import { ToasterModule } from 'angular2-toaster';
import {TeacherService} from "./services/teacher.service"

@NgModule({
  imports: [
    ThemeModule,
    Ng2SmartTableModule,
    ToasterModule.forRoot(),
  ],
  declarations: [
    ExamsComponent,
    NotificationsComponent,
  ],
  providers: [
    TeacherService
  ],
})
export class ExamsModule { }

