import { Component } from '@angular/core';
import { AuthService, CompanyAuthData } from '../../../services/auth.service';
import { LojaService } from '../../../services/loja.service';
import { BehaviorSubject } from 'rxjs';
import { User } from '../../../models/models';



@Component({
  selector: 'app-clientes',
  standalone: true,
  imports: [],
  templateUrl: './clientes.component.html',
  styleUrl: './clientes.component.sass'
})
export class ClientesComponent {

  clientes = new BehaviorSubject<Array<User>>([])
  companyData: CompanyAuthData

  constructor(
    private authService: AuthService,
    private lojaService: LojaService
  ) {
    let data = this.authService.currentCompany()

    if (!data) {
      let msg = 'Dados da Loja não encontrados!'
      alert(msg); throw new Error(msg)
    } else {
      this.companyData = data
    }

  }

  ngOnInit() {
    this.lojaService.getAllCostumers(this.companyData).subscribe({
      next: (result: any) => {
        let clientes = result.map((data: any) => new User(data))
        this.clientes.next(clientes)
      },
      error: (result) => {
        console.log(result)
      }
    })
  }

}
