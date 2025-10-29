"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

type VerificationStatus = "loading" | "success" | "error" | "already_verified";

export default function VerifyEmailPage() {
    const params = useParams();
    const router = useRouter();
    const token = params.token as string;

    const [status, setStatus] = useState<VerificationStatus>("loading");
    const [subscriberName, setSubscriberName] = useState<string>("");
    const [errorMessage, setErrorMessage] = useState<string>("");

    useEffect(() => {
        const verifyEmail = async () => {
            if (!token) {
                setStatus("error");
                setErrorMessage("Token de verificação não encontrado");
                return;
            }

            try {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/subscribers/verify-email/${token}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                        },
                    }
                );

                if (!response.ok) {
                    const data = await response.json();
                    if (data.detail?.includes("already verified")) {
                        setStatus("already_verified");
                    } else {
                        setStatus("error");
                        setErrorMessage(
                            data.detail ||
                            "Não foi possível verificar seu email. O link pode estar expirado."
                        );
                    }
                    return;
                }

                const data = await response.json();
                setSubscriberName(data.name || "");
                setStatus("success");

                // Redirecionar para home após 5 segundos
                setTimeout(() => {
                    router.push("/");
                }, 5000);
            } catch (error) {
                setStatus("error");
                setErrorMessage(
                    "Erro ao conectar com o servidor. Tente novamente mais tarde."
                );
                console.error("Verification error:", error);
            }
        };

        verifyEmail();
    }, [token, router]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#667eea] flex items-center justify-center px-4 py-20">
            <div className="max-w-2xl w-full">
                {/* Loading State */}
                {status === "loading" && (
                    <div className="bg-white/10 backdrop-blur-xl shadow-2xl rounded-3xl p-12 text-center">
                        <div className="flex justify-center mb-6">
                            <svg
                                className="animate-spin h-16 w-16 text-white"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                            >
                                <circle
                                    className="opacity-25"
                                    cx="12"
                                    cy="12"
                                    r="10"
                                    stroke="currentColor"
                                    strokeWidth="4"
                                ></circle>
                                <path
                                    className="opacity-75"
                                    fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                ></path>
                            </svg>
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-3">
                            Verificando seu email...
                        </h1>
                        <p className="text-white/80 text-lg">
                            Aguarde um momento enquanto confirmamos seu cadastro
                        </p>
                    </div>
                )}

                {/* Success State */}
                {status === "success" && (
                    <div className="bg-white/10 backdrop-blur-xl shadow-2xl rounded-3xl p-12 text-center">
                        <div className="w-24 h-24 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                            <svg
                                className="w-12 h-12 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={3}
                                    d="M5 13l4 4L19 7"
                                />
                            </svg>
                        </div>
                        <h1 className="text-4xl font-bold text-white mb-4">
                            ✅ Email Confirmado com Sucesso!
                        </h1>
                        {subscriberName && (
                            <p className="text-2xl text-white/90 mb-6">
                                Bem-vindo(a), {subscriberName}! 🎉
                            </p>
                        )}
                        <p className="text-xl text-white/80 mb-4">
                            Sua inscrição foi confirmada com sucesso!
                        </p>
                        <p className="text-lg text-white/70 mb-8">
                            Você começará a receber nossas ofertas exclusivas em breve.
                        </p>

                        <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-6 mb-8">
                            <p className="text-white/90 text-lg mb-2">📬 Fique de olho no seu email!</p>
                            <p className="text-white/70">
                                Em breve você receberá ofertas incríveis com até 70% de desconto
                            </p>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Link
                                href="/"
                                className="bg-gradient-to-r from-[#283593] to-[#1976d2] text-white font-bold py-4 px-8 rounded-xl hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-200 text-lg"
                            >
                                Voltar para a página inicial
                            </Link>
                        </div>

                        <p className="text-white/60 text-sm mt-6">
                            Você será redirecionado automaticamente em 5 segundos...
                        </p>
                    </div>
                )}

                {/* Already Verified State */}
                {status === "already_verified" && (
                    <div className="bg-white/10 backdrop-blur-xl shadow-2xl rounded-3xl p-12 text-center">
                        <div className="w-24 h-24 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                            <svg
                                className="w-12 h-12 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                />
                            </svg>
                        </div>
                        <h1 className="text-4xl font-bold text-white mb-4">
                            Email Já Verificado
                        </h1>
                        <p className="text-xl text-white/80 mb-8">
                            Este email já foi confirmado anteriormente. Você já está inscrito em nossa newsletter!
                        </p>
                        <Link
                            href="/"
                            className="inline-block bg-gradient-to-r from-[#283593] to-[#1976d2] text-white font-bold py-4 px-8 rounded-xl hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-200 text-lg"
                        >
                            Voltar para a página inicial
                        </Link>
                    </div>
                )}

                {/* Error State */}
                {status === "error" && (
                    <div className="bg-white/10 backdrop-blur-xl shadow-2xl rounded-3xl p-12 text-center">
                        <div className="w-24 h-24 bg-gradient-to-br from-red-400 to-red-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                            <svg
                                className="w-12 h-12 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                        </div>
                        <h1 className="text-4xl font-bold text-white mb-4">
                            ❌ Erro na Verificação
                        </h1>
                        <p className="text-xl text-white/80 mb-8">{errorMessage}</p>

                        <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-6 mb-8">
                            <p className="text-white/90 text-lg mb-2">💡 O que fazer?</p>
                            <ul className="text-white/70 text-left space-y-2 max-w-md mx-auto">
                                <li>✓ O link pode ter expirado (válido por 24 horas)</li>
                                <li>✓ Tente se inscrever novamente</li>
                                <li>✓ Verifique se copiou o link completo</li>
                            </ul>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Link
                                href="/"
                                className="bg-gradient-to-r from-[#283593] to-[#1976d2] text-white font-bold py-4 px-8 rounded-xl hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-200 text-lg"
                            >
                                Tentar Novamente
                            </Link>
                        </div>
                    </div>
                )}

                {/* OfertaBR Logo */}
                <div className="text-center mt-8">
                    <Link href="/" className="text-white/80 hover:text-white transition-colors">
                        <h2 className="text-3xl font-bold">OfertaBR</h2>
                        <p className="text-sm text-white/60 mt-2">
                            As melhores ofertas do Brasil 🇧🇷
                        </p>
                    </Link>
                </div>
            </div>
        </div>
    );
}

