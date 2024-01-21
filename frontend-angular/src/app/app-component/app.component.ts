import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterModule, Router } from '@angular/router';
import { NavbarComponent } from '../components/navbar/navbar.component';
import { AuthService } from '../services/auth.service';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    RouterModule,
    NavbarComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.sass'
})
export class AppComponent {
  title = 'frontend-angular';

  constructor(
    private authService: AuthService
  ) { };

  ngOnInit() {
    let data = this.authService.companyData.getValue()

    if (data && data.access_token){
      this.authService.refreshTokenData()
    }
  }

}
