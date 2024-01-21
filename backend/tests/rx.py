import reactivex as rx
import httpx
import time


class LojaService:
    def get_lojas(self, observer: rx.Observer, scheduler):
        observer.on_next(
            httpx.get('http://localhost:8000/loja/').json()
        )

        observer.on_completed()

    def get_value(self, value):
        print("Received {0}".format(value))

    def error_on_get_value(self, value):
        print("Error Occurred: {0}".format(value))

    def completed_on_get_value(self):
        print("Done!")

    def main(self):
        rx.create(self.get_lojas).subscribe(  # type: ignore
            on_next=self.get_value,
            on_error=self.error_on_get_value,
            on_completed=self.completed_on_get_value,
        )


class ProdutoService:
    def get_produtos(self, observer: rx.Observer, scheduler):
        observer.on_next(
            httpx.get('http://localhost:8000/produtos/').json()
        )

        observer.on_completed()

    def get_value(self, value):
        print("Received {0}".format(value))

    def error_on_get_value(self, value):
        print("Error Occurred: {0}".format(value))

    def completed_on_get_value(self):
        print("Done!")

    def main(self):
        rx.create(self.get_produtos).subscribe(  # type: ignore
            on_next=self.get_value,
            on_error=self.error_on_get_value,
            on_completed=self.completed_on_get_value,
        )


s1 = LojaService()
s2 = ProdutoService()

print(time.perf_counter())
s1.main()
print(time.perf_counter())
s2.main()
