import { ModuleWithProviders, NgModule, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbAuthModule, NbPasswordAuthStrategy,NbAuthJWTToken } from '@nebular/auth';
import { NbSecurityModule, NbRoleProvider } from '@nebular/security';
import { of as observableOf } from 'rxjs';

import { throwIfAlreadyLoaded } from './module-import-guard';
import { DataModule } from './data/data.module';
import { AnalyticsService } from './utils/analytics.service';
import {environment} from '../../environments/environment';

const socialLinks = [
  {
  },
];

export class NbSimpleRoleProvider extends NbRoleProvider {
  getRole() {
    // here you could provide any role based on any auth flow
    return observableOf('guest');
  }
}

export const NB_CORE_PROVIDERS = [
  ...DataModule.forRoot().providers,
  ...NbAuthModule.forRoot({

    strategies: [
      NbPasswordAuthStrategy.setup({
        name: 'phone_number',
        token: {
          class: NbAuthJWTToken,
          key: 'token',
        },

        baseEndpoint: environment.apiEndPoint,
        login: {
          endpoint: 'api-login-user',
          method: 'post',
        },
        logout: {
          endpoint: 'api-sign-out',
          method: 'post',
        },
        resetPass: {
          endpoint: 'api-reset-pass',
          method: 'post',
          redirect: {
            success: '/auth/login',
            failure: null,
          },
        },
      }),
    ],
    forms: {
      login: {
        redirectDelay: 500, // delay before redirect after a successful login, while success message is shown to the user
        strategy: 'phone_number',  // provider id key. If you have multiple strategies, or what to use your own
        rememberMe: true,   // whether to show or not the `rememberMe` checkbox
        showMessages: {     // show/not show success/error messages
          success: true,
          error: true,
        },
        socialLinks: socialLinks, // social links at the bottom of a page
      },
      register: {
        redirectDelay: 500,
        strategy: 'email',
        showMessages: {
          success: true,
          error: true,
        },
        terms: true,
        socialLinks: socialLinks,
      },
      requestPassword: {
        redirectDelay: 500,
        strategy: 'email',
        showMessages: {
          success: true,
          error: true,
        },
        socialLinks: socialLinks,
      },
      resetPassword: {
        redirectDelay: 500,
        strategy: 'phone_number',
        showMessages: {
          success: true,
          error: true,
        },
        socialLinks: socialLinks,
      },
      logout: {
        redirectDelay: 500,
        strategy: 'email',
      },
      validation: {
        password: {
          required: true,
          minLength: 4,
          maxLength: 50,
        },
        phone_number:{
          required:true,
          minLength: 10,
          maxLength: 10,
  
        },
        fullName: {
          required: false,
          minLength: 4,
          maxLength: 50,
        },
      },
    }
  }).providers,

  NbSecurityModule.forRoot({
    accessControl: {
      guest: {
        view: '*',
      },
      user: {
        parent: 'guest',
        create: '*',
        edit: '*',
        remove: '*',
      },
    },
  }).providers,

  {
    provide: NbRoleProvider, useClass: NbSimpleRoleProvider,
  },
  AnalyticsService,
];

@NgModule({
  imports: [
    CommonModule,
  ],
  exports: [
    NbAuthModule,
  ],
  declarations: [],
})
export class CoreModule {
  constructor(@Optional() @SkipSelf() parentModule: CoreModule) {
    throwIfAlreadyLoaded(parentModule, 'CoreModule');
  }

  static forRoot(): ModuleWithProviders {
    return <ModuleWithProviders>{
      ngModule: CoreModule,
      providers: [
        ...NB_CORE_PROVIDERS,
      ],
    };
  }
}
