import Link from "next/link";

interface FooterLinkProps {
    href: string;
    children: React.ReactNode;
}

function FooterLink({ href, children }: FooterLinkProps) {
    return (
        <li>
            <Link href={href} className="hover:text-white transition-colors">
                {children}
            </Link>
        </li>
    );
}

interface FooterSectionProps {
    title: string;
    children: React.ReactNode;
}

function FooterSection({ title, children }: FooterSectionProps) {
    return (
        <div>
            <h4 className="font-bold mb-4">{title}</h4>
            <ul className="space-y-2 text-gray-400">{children}</ul>
        </div>
    );
}

export function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-gray-900 text-white py-12 px-4">
            <div className="max-w-6xl mx-auto">
                <div className="grid md:grid-cols-3 gap-8 mb-8">
                    <div>
                        <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-[#667eea] to-[#764ba2] bg-clip-text text-transparent">
                            OfertaBR
                        </h3>
                        <p className="text-gray-400">
                            As melhores ofertas da internet na sua caixa de entrada.
                        </p>
                    </div>

                    <FooterSection title="Links Rápidos">
                        <FooterLink href="/sobre">Sobre</FooterLink>
                        <FooterLink href="/planos">Planos</FooterLink>
                        <FooterLink href="/contato">Contato</FooterLink>
                    </FooterSection>

                    <FooterSection title="Legal">
                        <FooterLink href="/termos">Termos de Uso</FooterLink>
                        <FooterLink href="/privacidade">Política de Privacidade</FooterLink>
                        <FooterLink href="/cancelar-inscricao">Cancelar Inscrição</FooterLink>
                    </FooterSection>
                </div>

                <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
                    <p>&copy; {currentYear} OfertaBR. Todos os direitos reservados.</p>
                    <p className="mt-2 text-sm">Feito com 💜 para você economizar</p>
                </div>
            </div>
        </footer>
    );
}

