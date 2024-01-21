import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService, SignupService, ViaCepService } from '../../../services/services';
import { Response201Wrapper } from '../../../models/models';
import { NgxMaskDirective } from 'ngx-mask';
import { ButtonHandler } from '../../../handlers/button';

@Component({
  selector: 'app-signup-user',
  standalone: true,
  imports: [FormsModule, NgxMaskDirective],
  templateUrl: './signup-user.component.html',
  styleUrl: './signup-user.component.sass'
})
export class SignupUserComponent {

  usernameValue: string
  emailValue: string
  passwordValue: string
  password2Value: string
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


  constructor(
    private service: SignupService,
    private authService: AuthService,
    private viaCepService: ViaCepService
  ) {
    this.usernameValue = ''
    this.emailValue = ''
    this.passwordValue = ''
    this.password2Value = ''
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
    let button = new ButtonHandler(event)
    button.disable('Cadastrando...')

    if (this.passwordValue != this.password2Value) {
      alert('A senha e a confirmação não são iguais')
      return
    }

    let body = {

      celular: this.celularValue,
      email: this.emailValue,
      nome: this.nomeValue,
      password: this.passwordValue,
      telefone: this.telefoneValue,
      username: this.usernameValue,

      bairro: this.bairroValue,
      cep: this.cepValue,
      cidade: this.cidadeValue,
      complemento: this.complementoValue,
      logradouro: this.logradouroValue,
      numero: this.numeroValue,
      uf: this.ufValue,

      modo_de_cadastro: 'auto_cadastro'

    }

    this.service.doUserSignUp(body).subscribe({
      next: (response) => {
        button.enable()
        let r = new Response201Wrapper(response)
        alert("Cadastro realizado com sucesso!")
        this.authService.doUserLogin(this.usernameValue, this.passwordValue)
      },
      error: (response) => {
        button.enable()
        let msg = "Erro no processamento dos dados!"
        alert(msg); throw new Error(msg)
      }
    })
  }


}
