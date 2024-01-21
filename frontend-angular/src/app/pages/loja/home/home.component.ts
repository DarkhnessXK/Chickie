import { Component } from '@angular/core';
import { AuthService, CompanyAuthData } from '../../../services/services';
import { BehaviorSubject } from 'rxjs';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [SpinnerComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.sass'
})
export class LojaHomeComponent {
  companyData: BehaviorSubject<CompanyAuthData | null>
  imageBase64String: string

  constructor (private authService: AuthService) {
    this.imageBase64String = '';
    this.companyData = this.authService.companyData
    if (this.companyData.value) {
      this.imageBase64String = this.companyData.value.loja.imagem_cadastro
    }
  }


}
