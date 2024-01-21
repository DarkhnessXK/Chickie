import { Component } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { UploadImageDataResponse, FileDataRequest } from '../../../models/models';
import { BehaviorSubject } from 'rxjs';
import { NgxMaskDirective } from 'ngx-mask';
import { ButtonHandler } from '../../../handlers/button';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';

import {  FormGroup, FormBuilder,
          ReactiveFormsModule, FormsModule } from '@angular/forms';

import {  LojaService, AuthService,
          CompanyAuthData, ImageService, ViaCepService } from '../../../services/services';

@Component({
  selector: 'app-loja-settings',
  standalone: true,
  imports: [ReactiveFormsModule, FormsModule, NgxMaskDirective, SpinnerComponent],
  templateUrl: './loja-settings.component.html',
  styleUrl: './loja-settings.component.sass'
})
export class LojaSettingsComponent {

  imageForm: FormGroup
  file: FileDataRequest
  atualizandoCadastro: boolean
  companyData: BehaviorSubject<CompanyAuthData | null>
  imageBase64String: string
  ufs: Array<string>
  uf: string

  nomeValue: string
  emailValue: string
  usernameValue: string
  cidadeValue: string
  bairroValue: string
  logradouroValue: string
  numeroValue: string
  complementoValue: string
  horariosValue: string
  celularValue: string
  telefoneValue: string
  cep: string

  constructor(
    private formBuilder: FormBuilder,
    private imageService: ImageService,
    private lojaService: LojaService,
    private authService: AuthService,
    private viaCepService: ViaCepService
  ) {

    this.celularValue = ''
    this.horariosValue = ''
    this.nomeValue = ''
    this.emailValue = ''
    this.usernameValue = ''
    this.cidadeValue = ''
    this.bairroValue = ''
    this.logradouroValue = ''
    this.numeroValue = ''
    this.complementoValue = ''
    this.telefoneValue = ''
    this.cep = ''

    this.atualizandoCadastro = false
    this.uf = ''
    this.ufs = [
      'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF',
      'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
      'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS',
      'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ];
    this.companyData = this.authService.companyData

    if (this.companyData.value) {

      this.cep = this.companyData.value.loja.endereco.cep
      this.nomeValue = this.companyData.value.loja.nome
      this.emailValue = this.companyData.value.loja.email
      this.usernameValue = this.companyData.value.loja.username
      this.cidadeValue = this.companyData.value.loja.endereco.cidade
      this.bairroValue = this.companyData.value.loja.endereco.bairro
      this.logradouroValue = this.companyData.value.loja.endereco.logradouro
      this.numeroValue = this.companyData.value.loja.endereco.numero
      this.complementoValue = this.companyData.value.loja.endereco.complemento
      this.celularValue = this.companyData.value.loja.celular
      this.horariosValue = this.companyData.value.loja.horarios_de_funcionamento || ''
      this.telefoneValue = this.companyData.value.loja.telefone

    }

    this.imageForm = this.formBuilder.group({ imageFile: [''] });
    this.file = { bytes_base64: '', filename: '' }
    if (!this.companyData.value) {
      let msg = 'Dados da loja não encontrados!';
      alert(msg); throw new Error(msg)
    }
    this.imageBase64String = this.companyData.value.loja.imagem_cadastro
  }

  ngOnInit() {
    for (let item of this.ufs) {
      if (item == this.companyData.value?.loja.endereco.uf) {
        this.uf = item
      }
    }
  }

  async onFileSelected(event: any) {
    const eventFile: File = event.target.files[0];
    if (eventFile) {
      this.file = {
        filename: eventFile.name,
        bytes_base64: await this.imageService.getImageBytes(eventFile)

      }
    }
  }

  getCEPData() {
    const numerosEncontrados = this.cep.match(/\d/g);
    console.log({numerosEncontrados: numerosEncontrados})
    if (numerosEncontrados?.length == 8) {
      this.viaCepService.getAddressInfo(this.cep).subscribe({
        next: (result: any) => {
          console.log({erro: result.erro})
          if (result.erro) {
            throw new Error('CEP inválido')
          }

          this.viaCepService.setCachedData(result)
          console.log({result: result})
          this.logradouroValue = result.logradouro
          this.bairroValue = result.bairro
          this.cidadeValue = result.localidade
          this.uf = result.uf
        },
        error: (result) => {
          alert('Erro na requisição')
        }
      })
    }
  }

  uploadImage(event: Event) {
    let button = new ButtonHandler(event)
    button.disable('Atualizando...')
    console.log(this.file)
    let companyData = this.authService.companyData.getValue()

    if (!companyData) {
      button.enable()
      let msg = 'Dados da loja não encontrados!'
      alert(msg); throw new Error(msg)
    }


    this.lojaService.atualizarImagemCadastro(this.file, companyData).subscribe({
      next: (response: any) => {
        button.enable()
        let result: UploadImageDataResponse = {...response.result}

        if (!this.companyData.value) {

          let msg = 'Dados de autenticação não encontrados!';
          alert(msg); throw new Error(msg);
        }

        this.companyData.value.loja.imagem_cadastro = result.data.secure_url
        this.authService.setCompanyData(this.companyData.value)

        alert('Imagem atualizada com sucesso!')

      },
      error: (result: HttpErrorResponse) => {
        button.enable()
        console.log({result: result.error})
        alert('Erro no upload da imagem!')
      }
    })
  }

  atualizarCadastro(event: Event) {

    let button = new ButtonHandler(event)
    button.disable('Atualizando...')

    this.atualizandoCadastro = true
    let companyData = this.authService.companyData.getValue()

    if (!companyData) {
      let msg = 'Dados da loja não encontrados!'
      alert(msg); throw new Error(msg)
    }

    let body = {

      email: this.emailValue,
      telefone: this.telefoneValue,
      celular: this.celularValue,

      nome: this.nomeValue,
      username: this.usernameValue,

      uf: this.uf,
      cep: this.cep,
      cidade: this.cidadeValue,
      logradouro: this.logradouroValue,
      bairro: this.bairroValue,
      numero: this.numeroValue,
      complemento: this.complementoValue,

      horarios_de_funcionamento: this.horariosValue,
    }

    this.lojaService.atualizarCadastro(body, companyData).subscribe({
      next: (response) => {
        button.enable()
        console.log({response: response})

        this.authService.refreshLojaData()
        alert('Cadastro atualizado com sucesso!')
      },
      error: (result: HttpErrorResponse) => {
        button.enable()
        console.log({result: result.error})
        alert('Erro na atualização dos dados!')
      }
    })
  }
}
