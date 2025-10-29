import { Footer } from "@/app/components";

export const metadata = {
    title: "Contato - OfertaBR",
    description: "Entre em contato conosco",
};

function ContactInfo() {
    return (
        <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Informações de Contato
            </h2>

            <div className="space-y-4">
                <div className="flex items-start">
                    <div className="text-2xl mr-4">📧</div>
                    <div>
                        <h3 className="font-bold text-gray-900">Email</h3>
                        <p className="text-gray-600">contato@ofertabr.com.br</p>
                    </div>
                </div>

                <div className="flex items-start">
                    <div className="text-2xl mr-4">💬</div>
                    <div>
                        <h3 className="font-bold text-gray-900">WhatsApp</h3>
                        <p className="text-gray-600">+55 (11) 98765-4321</p>
                    </div>
                </div>

                <div className="flex items-start">
                    <div className="text-2xl mr-4">⏰</div>
                    <div>
                        <h3 className="font-bold text-gray-900">Horário de Atendimento</h3>
                        <p className="text-gray-600">Segunda a Sexta, 9h às 18h</p>
                    </div>
                </div>
            </div>

            <div className="mt-8 pt-8 border-t border-gray-200">
                <h3 className="font-bold text-gray-900 mb-4">Redes Sociais</h3>
                <div className="flex space-x-4">
                    <a
                        href="#"
                        className="text-3xl hover:scale-110 transition-transform"
                        aria-label="Instagram"
                    >
                        📸
                    </a>
                    <a
                        href="#"
                        className="text-3xl hover:scale-110 transition-transform"
                        aria-label="Twitter"
                    >
                        🐦
                    </a>
                    <a
                        href="#"
                        className="text-3xl hover:scale-110 transition-transform"
                        aria-label="Facebook"
                    >
                        📘
                    </a>
                </div>
            </div>
        </div>
    );
}

export default function ContatoPage() {
    return (
        <main className="min-h-screen">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#667eea] text-white py-20 px-4">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">
                        Entre em Contato
                    </h1>
                    <p className="text-xl md:text-2xl text-white/90">
                        Estamos aqui para ajudar você!
                    </p>
                </div>
            </section>

            {/* Contact Section */}
            <section className="py-20 px-4 bg-gray-50">
                <div className="max-w-5xl mx-auto">
                    <div className="grid md:grid-cols-2 gap-8">
                        {/* Contact Form */}
                        <div className="bg-white rounded-2xl shadow-lg p-8">
                            <h2 className="text-2xl font-bold text-gray-900 mb-6">
                                Envie uma Mensagem
                            </h2>
                            <form className="space-y-4">
                                <div>
                                    <label className="block text-gray-700 font-medium mb-2">
                                        Nome
                                    </label>
                                    <input
                                        type="text"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#667eea] focus:border-transparent outline-none"
                                        placeholder="Seu nome completo"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-700 font-medium mb-2">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#667eea] focus:border-transparent outline-none"
                                        placeholder="seu@email.com"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-700 font-medium mb-2">
                                        Assunto
                                    </label>
                                    <select
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#667eea] focus:border-transparent outline-none"
                                        id="assunto"
                                        name="assunto"
                                        required
                                        aria-label="Selecione o assunto"
                                    >
                                        <option value="">Selecione o assunto</option>
                                        <option>Dúvida sobre o serviço</option>
                                        <option>Suporte técnico</option>
                                        <option>Parceria</option>
                                        <option>Outro</option>
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-gray-700 font-medium mb-2">
                                        Mensagem
                                    </label>
                                    <textarea
                                        rows={5}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#667eea] focus:border-transparent outline-none resize-none"
                                        placeholder="Escreva sua mensagem aqui..."
                                        required
                                    ></textarea>
                                </div>

                                <button
                                    type="submit"
                                    className="w-full bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-bold py-4 px-6 rounded-lg hover:shadow-xl transition-all duration-200"
                                >
                                    Enviar Mensagem 📤
                                </button>
                            </form>
                        </div>

                        {/* Contact Info */}
                        <ContactInfo />
                    </div>
                </div>
            </section>

            <Footer />
        </main>
    );
}

