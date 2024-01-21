import { Component } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { Response201Wrapper, StatusResponse } from '../../../models/models';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';

import {  AuthService, CompanyAuthData,
          StatusService } from '../../../services/services';
import { ButtonHandler } from '../../../handlers/button';


@Component({
  selector: 'app-status',
  standalone: true,
  imports: [FormsModule, SpinnerComponent],
  templateUrl: './status.component.html',
  styleUrl: './status.component.sass'
})
export class StatusComponent {

  companyData: CompanyAuthData | null
  statusList: BehaviorSubject<Array<StatusResponse>>
  descricaoValue: string
  nomeValue: string
  saving: boolean
  fetching: boolean

  constructor(private statusService: StatusService, private authService: AuthService) {
    this.saving = false
    this.fetching = false
    this.descricaoValue = ''
    this.nomeValue = ''
    this.companyData = authService.currentCompany();
    this.statusList = new BehaviorSubject<Array<StatusResponse>>([])
  }

  ngOnInit(): void {
    this.fetching = true
    if (this.companyData === null) {
      let msg = 'Dados da empresa não encontrados!'
      alert(msg); throw new Error(msg)
    }
    this.statusService.getAll(this.companyData.loja.uuid).subscribe({
      next: (result: any) => {
        let payload = result.payload
        if (Array.isArray(payload)) {
          this.statusList.value.push(...payload)
        }
        this.fetching = false
      },
      error: (result) => {
        throw new Error('Erro na requisição dos dados')
      }
    })

  }

  public cadastrarStatus(): void {
    this.saving = true
    if (!this.companyData) {
      this.saving = false
      let msg = 'Dados da empresa não encontrados!'
      alert(msg); throw new Error(msg)
    }

    let body = {
      loja_uuid: this.companyData.loja.uuid,
      descricao: this.descricaoValue,
      nome: this.nomeValue
    }

    this.statusService.save(body).subscribe({
      next: (response) => {
        let r = new Response201Wrapper(response)
        let newStatusItem = {...body, uuid: r.uuid}
        this.statusList.value.push(newStatusItem)
        alert('Item cadastrado com sucesso!')
        this.saving = false
      },
      error: (response) => {
        this.saving = false
        let msg = 'Erro no cadastro do item';
        alert(msg); throw new Error(msg)
      }
    })
  }

  public deletarStatus(event: Event, status: StatusResponse): void {

    let button = new ButtonHandler(event)
    button.disable('Removendo...')

    this.statusService.delete(status).subscribe({
      next: (response) => {
        button.enable()
        let newList = this.statusList.value
        .filter(item => item.uuid !== status.uuid);

        this.statusList.next(newList);
        alert('Item removido com sucesso!')
      },
      error: (response) => {
        let msg = 'Erro na remoção do item. Algum pedido pode estar vinculado';

        button.enable()

        alert(msg); throw new Error(msg)
      }
    })
  }
}
