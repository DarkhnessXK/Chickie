import { Component } from '@angular/core';
import { SignupService } from '../../../services/signup.service';
import { AuthService, CompanyAuthData } from '../../../services/auth.service';
import { ViaCepService } from '../../../services/viacep.service';
import { FormsModule } from '@angular/forms';
import { NgxMaskDirective } from 'ngx-mask';
import { Response201Wrapper } from '../../../models/wrapper';
import { ButtonHandler } from '../../../handlers/button';
import { LojaService } from '../../../services/loja.service';

@Component({
  selector: 'app-cadastro-cliente',
  standalone: true,
  imports: [FormsModule, NgxMaskDirective],
  templateUrl: './cadastro-cliente.component.html',
  styleUrl: './cadastro-cliente.component.sass'
})
export class CadastroClienteComponent {

  usernameValue: string
  emailValue: string
  nomeValue: string
  celularValue: string
  telefoneValue: string
  cepValue: string
  logradouroValue: string
  numeroValue: string
  complementoValue: string
  bairroValue: string
  cidadeValue: string
  ufValue: string
  companyData: CompanyAuthData | null

  constructor(
    private service: SignupService,
    private authService: AuthService,
    private viaCepService: ViaCepService,
    private lojaService: LojaService
  ) {
    this.companyData = this.authService.currentCompany()
    this.usernameValue = ''
    this.emailValue = ''
    this.nomeValue = ''
    this.celularValue = ''
    this.telefoneValue = ''
    this.cepValue = ''
    this.logradouroValue = ''
    this.numeroValue = ''
    this.complementoValue = ''
    this.bairroValue = ''
    this.cidadeValue = ''
    this.ufValue = ''
  }

  getCEPData() {
    console.log({'this.cepValue': this.cepValue})
    const numerosEncontrados = this.cepValue.match(/\d/g);
    if (numerosEncontrados?.length == 8) {
      this.viaCepService.getAddressInfo(this.cepValue).subscribe({
        next: (result: any) => {
          this.viaCepService.setCachedData(result)
          this.logradouroValue = result.logradouro
          this.bairroValue = result.bairro
          this.cidadeValue = result.localidade
          this.ufValue = result.uf
        },
        error: (result) => {
          alert('Erro na requisição')
        }
      })
    }
  }

  doSignUp(event: Event) {

    if (!this.companyData) {
      let msg = 'Dados da empresa não encontrados!'
      alert(msg); throw new Error(msg)
    }

    let button = new ButtonHandler(event)
    button.disable('Cadastrando...')

    let body = {

      celular: this.celularValue,
      email: this.emailValue,
      nome: this.nomeValue,
      password: '123456',
      telefone: this.telefoneValue,
      username: this.usernameValue,

      bairro: this.bairroValue,
      cep: this.cepValue,
      cidade: this.cidadeValue,
      complemento: this.complementoValue,
      logradouro: this.logradouroValue,
      numero: this.numeroValue,
      uf: this.ufValue,

      modo_de_cadastro: 'cadastro_de_loja'

    }

    this.lojaService.cadastrarUser(
      this.companyData.loja.uuid,
      body,
      this.companyData
    ).subscribe({
      next: (response) => {
        button.enable()
        let r = new Response201Wrapper(response)
        alert("Cadastro realizado com sucesso!")
        this.clearInputs()
      },
      error: (response) => {
        button.enable()
        let msg = "Erro no processamento dos dados!"
        alert(msg); throw new Error(msg)
      }
    })
  }

  clearInputs() {
    this.usernameValue = ''
    this.emailValue = ''
    this.nomeValue = ''
    this.celularValue = ''
    this.telefoneValue = ''
    this.cepValue = ''
    this.logradouroValue = ''
    this.numeroValue = ''
    this.complementoValue = ''
    this.bairroValue = ''
    this.cidadeValue = ''
    this.ufValue = ''
  }

}
